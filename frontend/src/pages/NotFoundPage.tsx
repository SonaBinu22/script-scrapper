import React from 'react';
import { HelpCircle, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="max-w-md mx-auto my-20 p-8 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-4">
      <div className="mx-auto w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center text-rose-400">
        <HelpCircle className="w-6 h-6" />
      </div>
      <h2 className="text-2xl font-bold text-white">Page Not Found</h2>
      <p className="text-xs text-slate-400">
        The requested URL was not found in the Script Scrapper SPA.
      </p>
      <div className="pt-2">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Safety
        </Link>
      </div>
    </div>
  );
};
