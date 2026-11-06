import React from 'react';
import { ShieldCheck, Download } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-400">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Script Scrapper &bull; Windows-Hosted Multi-User Screenplay Extraction System</span>
        </div>

        <div className="flex items-center space-x-4">
          <a
            href="/system/ca.crt"
            download="script-scrapper-ca.crt"
            className="flex items-center space-x-1.5 text-emerald-400 hover:text-emerald-300 font-mono underline decoration-emerald-500/50 hover:decoration-emerald-400"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Caddy Root CA</span>
          </a>
          <span className="text-slate-600">|</span>
          <span className="font-mono text-slate-400">Gate 1: Foundation Baseline v1.3</span>
        </div>
      </div>
    </footer>
  );
};
