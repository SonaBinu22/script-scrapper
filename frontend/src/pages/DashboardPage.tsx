import React from 'react';
import { FolderGit2, Plus, FileText, AlertCircle, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6 py-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <FolderGit2 className="w-6 h-6 text-emerald-400" />
            Project Workspace Shell
          </h1>
          <p className="text-xs text-slate-400 mt-1">Multi-User Screenplay Breakdown Projects</p>
        </div>
        <button
          type="button"
          disabled
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 border border-slate-700 text-slate-500 font-medium text-xs cursor-not-allowed"
        >
          <Plus className="w-4 h-4" />
          New Project (Gate 2)
        </button>
      </div>

      <div className="p-4 rounded-lg bg-blue-950/30 border border-blue-800/50 text-xs space-y-2">
        <div className="flex items-center gap-2 font-semibold text-blue-300">
          <AlertCircle className="w-4 h-4" />
          <span>Gate 1 Foundation Workspace Shell</span>
        </div>
        <p className="text-blue-200/80 leading-relaxed">
          Project CRUD, screenplay ingestion (searchable & scanned PDFs), OCR queue management, and scene breakdown extraction will be implemented in subsequent development gates.
        </p>
      </div>

      {/* Empty State Mock */}
      <div className="rounded-xl border border-dashed border-slate-800 p-12 text-center space-y-4 bg-slate-900/30">
        <div className="mx-auto w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center text-slate-500">
          <FileText className="w-6 h-6" />
        </div>
        <div className="max-w-sm mx-auto space-y-1">
          <h3 className="text-sm font-semibold text-white">No active screenplays loaded</h3>
          <p className="text-xs text-slate-400">
            Screenplay versioning tables (14 tables + indexes) are initialized and ready in PostgreSQL 16.
          </p>
        </div>
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-xs text-emerald-400 hover:text-emerald-300 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Return to System Diagnostics
        </Link>
      </div>
    </div>
  );
};
