import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FileText, Activity } from 'lucide-react';
import { fetchHealth } from '../api/client';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    let mounted = true;
    const check = async () => {
      const healthy = await fetchHealth();
      if (mounted) setIsBackendHealthy(healthy);
    };
    check();
    const interval = setInterval(check, 10000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  const navLinks = [
    { to: '/', label: 'Overview' },
    { to: '/dashboard', label: 'Workspace Shell' },
    { to: '/login', label: 'Sign In' },
    { to: '/register', label: 'Register' },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-3 text-white font-bold text-lg hover:opacity-90 transition">
          <div className="h-9 w-9 rounded-lg bg-emerald-600 flex items-center justify-center text-white shadow-lg shadow-emerald-500/20">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <span className="tracking-tight">Script Scrapper</span>
            <span className="ml-2 text-xs font-mono font-medium px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
              Gate 1 Foundation
            </span>
          </div>
        </Link>

        {/* Backend Health Pill */}
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2 text-xs font-mono px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700">
            <Activity className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-slate-300">API Status:</span>
            {isBackendHealthy === null ? (
              <span className="text-amber-400">Checking...</span>
            ) : isBackendHealthy ? (
              <span className="text-emerald-400 flex items-center gap-1">
                <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                Online
              </span>
            ) : (
              <span className="text-rose-400 flex items-center gap-1">
                <span className="inline-block w-2 h-2 rounded-full bg-rose-500" />
                Degraded
              </span>
            )}
          </div>

          <nav className="flex items-center space-x-1 sm:space-x-2">
            {navLinks.map((item) => {
              const active = location.pathname === item.to;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`text-sm px-3 py-1.5 rounded-md transition font-medium ${
                    active
                      ? 'bg-slate-800 text-white border border-slate-700 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
