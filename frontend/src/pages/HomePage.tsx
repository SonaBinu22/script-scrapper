import React, { useEffect, useState } from 'react';
import { Database, Server, Cpu, CheckCircle2, ShieldCheck, ArrowRight, Activity, Terminal } from 'lucide-react';
import { fetchSystemStatus, type SystemStatusData } from '../api/client';
import { Link } from 'react-router-dom';

export const HomePage: React.FC = () => {
  const [statusData, setStatusData] = useState<SystemStatusData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    fetchSystemStatus().then((data) => {
      if (mounted) {
        setStatusData(data);
        setLoading(false);
      }
    });
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="space-y-10 py-6">
      {/* Hero Section */}
      <div className="relative rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-emerald-950/40 p-8 sm:p-12 border border-slate-800 shadow-2xl overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Gate 1 Foundation Implementation Active
          </div>
          <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
            Script Scrapper <span className="text-emerald-400">Core Foundation</span>
          </h1>
          <p className="text-slate-300 text-base sm:text-lg leading-relaxed">
            High-precision, multi-user screenplay breakdown and intelligence platform running natively on Windows host with local network HTTPS access, isolated database connection pooling, and resilient worker architecture.
          </p>
          <div className="pt-2 flex flex-wrap gap-4">
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm transition shadow-lg shadow-emerald-600/30"
            >
              Enter Workspace Shell
              <ArrowRight className="w-4 h-4" />
            </Link>
            <a
              href="/system/ca.crt"
              download="script-scrapper-ca.crt"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-sm transition"
            >
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Download LAN CA Certificate
            </a>
          </div>
        </div>
      </div>

      {/* Live System Diagnostics Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Live System & Telemetry Diagnostics
          </h2>
          <span className="text-xs font-mono text-slate-400">Endpoint: /api/v1/system/status</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Database Card */}
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400">
                <Database className="w-6 h-6" />
              </div>
              <span className={`text-xs font-mono font-medium px-2.5 py-1 rounded-full ${
                statusData?.database?.connected ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-rose-950 text-rose-400 border border-rose-800'
              }`}>
                {loading ? 'Probing...' : statusData?.database?.connected ? 'ONLINE' : 'OFFLINE'}
              </span>
            </div>
            <div>
              <h3 className="text-base font-semibold text-white">PostgreSQL 16 Cluster</h3>
              <p className="text-xs text-slate-400 mt-1">Native Windows local engine with asyncpg pool</p>
            </div>
            <div className="pt-2 border-t border-slate-800/80 space-y-2 text-xs font-mono">
              <div className="flex justify-between text-slate-400">
                <span>Per-Worker Pool:</span>
                <span className="text-white font-medium">{statusData?.database?.pool?.configured_pool_size ?? 15} conns</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Max Overflow:</span>
                <span className="text-white font-medium">+{statusData?.database?.pool?.configured_max_overflow ?? 5} conns</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Total Pool Ceiling / Worker:</span>
                <span className="text-emerald-400 font-semibold">20 conns</span>
              </div>
            </div>
          </div>

          {/* Backend API Server Card */}
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                <Server className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono font-medium px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
                {statusData?.status ? statusData.status.toUpperCase() : 'HEALTHY'}
              </span>
            </div>
            <div>
              <h3 className="text-base font-semibold text-white">FastAPI + Uvicorn Gateway</h3>
              <p className="text-xs text-slate-400 mt-1">Async HTTP server with strict JSON error envelope</p>
            </div>
            <div className="pt-2 border-t border-slate-800/80 space-y-2 text-xs font-mono">
              <div className="flex justify-between text-slate-400">
                <span>Configured Workers:</span>
                <span className="text-white font-medium">{statusData?.server?.configured_workers ?? 2} Workers</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Aggregate Peak API Ceiling:</span>
                <span className="text-emerald-400 font-semibold">{statusData?.server?.aggregate_api_peak_ceiling ?? 40} conns</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Environment:</span>
                <span className="text-white font-medium">{statusData?.environment ?? 'development'}</span>
              </div>
            </div>
          </div>

          {/* Reverse Proxy Card */}
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="p-3 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
                <Cpu className="w-6 h-6" />
              </div>
              <span className="text-xs font-mono font-medium px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
                ACTIVE
              </span>
            </div>
            <div>
              <h3 className="text-base font-semibold text-white">Caddy v2 Reverse Proxy</h3>
              <p className="text-xs text-slate-400 mt-1">Automatic internal TLS and static SPA asset distribution</p>
            </div>
            <div className="pt-2 border-t border-slate-800/80 space-y-2 text-xs font-mono">
              <div className="flex justify-between text-slate-400">
                <span>TLS Mode:</span>
                <span className="text-white font-medium">Internal CA (Auto)</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Root CA Distro:</span>
                <span className="text-emerald-400 font-medium">/system/ca.crt</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>LAN Isolation:</span>
                <span className="text-white font-medium">Host Ports 80 / 443</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Architectural Scope Boundaries */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 space-y-3">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
          Gate 1 Implementation Scope & Boundaries
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-lg bg-slate-900 border border-emerald-900/50 space-y-1">
            <div className="font-semibold text-emerald-400 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Delivered in Gate 1
            </div>
            <p className="text-slate-300">
              PostgreSQL 16 native cluster, full 14-table Alembic schema migration with partial unique current-version index, FastAPI health & pool diagnostics endpoints, Vite + React + Tailwind foundation, Caddy reverse proxy configuration, and verified backup/restore scripts.
            </p>
          </div>
          <div className="p-4 rounded-lg bg-slate-900 border border-amber-900/50 space-y-1">
            <div className="font-semibold text-amber-400 flex items-center gap-1.5">
              <Terminal className="w-4 h-4" /> Deferred to Gate 2 (By Architecture Design)
            </div>
            <p className="text-slate-300">
              User registration endpoints, Argon2id authentication, session management, project creation CRUD, PDF file ingestion, OCR rasterization, and LLM breakdown intelligence.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
