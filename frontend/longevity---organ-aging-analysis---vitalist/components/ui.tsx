import React from 'react';

export const Card: React.FC<{ children: React.ReactNode; className?: string; title?: string }> = ({ children, className = "", title }) => (
  <div className={`bg-white border border-slate-200 rounded-sm p-5 ${className}`}>
    {title && <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wide mb-4 border-b border-slate-100 pb-2">{title}</h3>}
    {children}
  </div>
);

export const Badge: React.FC<{ children: React.ReactNode; type?: 'neutral' | 'success' | 'warning' | 'danger' }> = ({ children, type = 'neutral' }) => {
  const styles = {
    neutral: 'bg-slate-100 text-slate-600',
    success: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    warning: 'bg-amber-50 text-amber-700 border-amber-100',
    danger: 'bg-rose-50 text-rose-700 border-rose-100',
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-medium border ${styles[type]}`}>
      {children}
    </span>
  );
};

export const SectionHeader: React.FC<{ title: string; subtitle?: string }> = ({ title, subtitle }) => (
  <div className="mb-6">
    <h2 className="text-2xl font-bold text-slate-900 tracking-tight">{title}</h2>
    {subtitle && <p className="text-slate-500 mt-1 max-w-3xl leading-relaxed">{subtitle}</p>}
  </div>
);

export const OrganLegendItem: React.FC<{ color: string; label: string }> = ({ color, label }) => (
  <div className="flex items-center space-x-2">
    <span className="w-3 h-3 rounded-full" style={{ backgroundColor: color }}></span>
    <span className="text-xs text-slate-600 font-medium">{label}</span>
  </div>
);
