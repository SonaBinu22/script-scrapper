from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from backend.app.core.config import settings

# Single Approved Database Connection Pool Strategy:
# SQLAlchemy 2.0 AsyncEngine with asyncpg driver
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,          # 15 connections per Uvicorn worker process
    max_overflow=settings.DB_MAX_OVERFLOW,    # 5 overflow connections per process (Max: 20 per process)
    pool_timeout=settings.DB_POOL_TIMEOUT,    # 30.0 seconds timeout
    pool_recycle=settings.DB_POOL_RECYCLE,    # 1800.0 seconds recycle
    pool_pre_ping=True,                       # Active test SELECT 1 socket check
    echo=settings.DB_ECHO,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def check_database_connectivity() -> dict:
    pool = engine.pool
    pool_stats = {
        "configured_pool_size": settings.DB_POOL_SIZE,
        "configured_max_overflow": settings.DB_MAX_OVERFLOW,
        "current_pool_size": pool.size(),
        "checked_in_connections": pool.checkedin(),
        "checked_out_connections": pool.checkedout(),
        "overflow_connections": pool.overflow(),
    }

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1;"))
            scalar = result.scalar()
            return {
                "connected": scalar == 1,
                "status": "online",
                "pool": pool_stats,
            }
    except Exception as e:
        return {
            "connected": False,
            "status": "error",
            "error_detail": str(e),
            "pool": pool_stats,
        }
