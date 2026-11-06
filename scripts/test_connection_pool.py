import asyncio
import httpx
import asyncpg
import time

DATABASE_DSN = "postgresql://postgres:postgres@127.0.0.1:5432/script_scrapper"
TARGET_URL = "https://localhost/api/v1/system/status"

async def check_pg_stats(conn):
    rows = await conn.fetch(
        """
        SELECT pid, usename, client_port, state, query, backend_start
        FROM pg_stat_activity
        WHERE datname = 'script_scrapper' AND pid <> pg_backend_pid();
        """
    )
    return rows

async def make_request(client, req_id):
    try:
        resp = await client.get(TARGET_URL)
        return resp.status_code, resp.json()
    except Exception as e:
        return 0, str(e)

async def run_load_test():
    print("=== Starting Connection Pool & Concurrency Load Verification ===")
    pg_conn = await asyncpg.connect(DATABASE_DSN)
    
    # 1. Baseline connection count
    initial_conns = await check_pg_stats(pg_conn)
    print(f"[Baseline] Active script_scrapper connections before load: {len(initial_conns)}")
    for r in initial_conns:
        print(f"  PID {r['pid']}: state={r['state']}, port={r['client_port']}")

    # 2. Fire 50 concurrent requests across Caddy load balancer
    concurrency = 50
    print(f"\n[Execution] Firing {concurrency} concurrent requests to {TARGET_URL}...")
    
    samples = []
    async def sample_loop():
        for _ in range(10):
            await asyncio.sleep(0.04)
            data = await check_pg_stats(pg_conn)
            samples.append(data)

    async with httpx.AsyncClient(verify=False, timeout=15.0) as client:
        sampler = asyncio.create_task(sample_loop())
        start_time = time.time()
        tasks = [make_request(client, i) for i in range(concurrency)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time
        await sampler

    status_codes = [r[0] for r in results]
    success_count = status_codes.count(200)
    print(f"[Results] Completed {concurrency} requests in {elapsed:.3f}s")
    print(f"  HTTP 200 OK: {success_count}/{concurrency}")
    print(f"  Failed: {concurrency - success_count}")

    # Inspect sampled in-flight connections
    peak_conns = max(len(s) for s in samples) if samples else 0
    print(f"\n[Sampling] Peak PostgreSQL server connections sampled during load: {peak_conns}")
    for idx, s in enumerate(samples):
        active_count = sum(1 for r in s if r['state'] == 'active')
        idle_count = sum(1 for r in s if r['state'] == 'idle')
        print(f"  Sample {idx+1}: Total={len(s)} (Active={active_count}, Idle={idle_count})")

    # 3. Post-load connection count & cleanup check
    await asyncio.sleep(1.0)
    post_conns = await check_pg_stats(pg_conn)
    print(f"\n[Post-Load] Active script_scrapper connections after 1s cooldown: {len(post_conns)}")
    for r in post_conns:
        print(f"  PID {r['pid']}: state={r['state']}, port={r['client_port']}")

    # 4. Check PostgreSQL Global Server Connection Limits
    max_conn_row = await pg_conn.fetchrow("SHOW max_connections;")
    res_conn_row = await pg_conn.fetchrow("SHOW superuser_reserved_connections;")
    total_active_all_dbs = await pg_conn.fetchval("SELECT count(*) FROM pg_stat_activity;")
    
    print("\n[PostgreSQL Global Budget Invariants]")
    print(f"  max_connections: {max_conn_row['max_connections']}")
    print(f"  superuser_reserved_connections: {res_conn_row['superuser_reserved_connections']}")
    print(f"  total connections across entire cluster: {total_active_all_dbs}")
    print(f"  Worker 1 pool ceiling: 20 (15 base + 5 overflow)")
    print(f"  Worker 2 pool ceiling: 20 (15 base + 5 overflow)")
    print(f"  Combined 2-Worker peak API ceiling: 40 connections")
    print(f"  Margin below PostgreSQL 100 limit: {int(max_conn_row['max_connections']) - 40} available slots")

    await pg_conn.close()

if __name__ == "__main__":
    asyncio.run(run_load_test())
