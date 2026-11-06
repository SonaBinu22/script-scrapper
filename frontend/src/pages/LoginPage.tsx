import React from 'react';
import { Lock, AlertCircle, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export const LoginPage: React.FC = () => {
  return (
    <div className="max-w-md mx-auto my-12 p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
      <div className="text-center space-y-2">
        <div className="mx-auto w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-emerald-400">
          <Lock className="w-6 h-6" />
        </div>
        <h2 className="text-2xl font-bold text-white">Sign In Shell</h2>
        <p className="text-xs text-slate-400">Script Scrapper Security Gateway</p>
      </div>

      <div className="p-4 rounded-lg bg-amber-950/40 border border-amber-800/60 text-xs space-y-2">
        <div className="flex items-center gap-2 font-semibold text-amber-300">
          <AlertCircle className="w-4 h-4" />
          <span>Gate 1 Foundation Boundary Notice</span>
        </div>
        <p className="text-amber-200/80 leading-relaxed">
          Authentication and session verification are strictly scheduled for Gate 2 per the System Architect's implementation plan. This UI shell validates client-side routing and style foundations.
        </p>
      </div>

      <form onSubmit={(e) => e.preventDefault()} className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Email Address</label>
          <input
            type="email"
            disabled
            placeholder="user@example.com"
            className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 text-sm cursor-not-allowed"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">Password</label>
          <input
            type="password"
            disabled
            placeholder="••••••••••••"
            className="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 text-sm cursor-not-allowed"
          />
        </div>
        <button
          type="button"
          disabled
          className="w-full py-2.5 rounded-lg bg-slate-800 text-slate-500 font-semibold text-sm cursor-not-allowed border border-slate-700"
        >
          Sign In (Disabled in Gate 1)
        </button>
      </form>

      <div className="text-center pt-2">
        <Link to="/" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to System Overview
        </Link>
      </div>
    </div>
  );
};
