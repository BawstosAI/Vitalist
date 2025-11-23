import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ScatterChart, Scatter, Cell, LineChart, Line } from 'recharts';
import { OrganMetric, CorrelationMatrix, Individual } from '../types';

const ORGAN_COLORS: Record<string, string> = {
  'Liver': '#d97706',
  'Kidney': '#0d9488',
  'Cardio-Metabolic': '#e11d48',
  'Immune': '#9333ea',
  'Hematologic': '#4f46e5',
  'Cardio': '#e11d48',
  'Heme': '#4f46e5',
};

// -- Custom Tooltip --
const ScientificTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-slate-200 p-2 shadow-sm rounded-sm text-xs">
        <p className="font-semibold mb-1 text-slate-700">{label}</p>
        {payload.map((p: any, idx: number) => (
          <div key={idx} className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: p.color }} />
            <span className="text-slate-600">{p.name}: {typeof p.value === 'number' ? p.value.toFixed(2) : p.value}</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

// -- Model Performance Chart --
export const PerformanceChart: React.FC<{ data: OrganMetric[] }> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
        <XAxis type="number" stroke="#64748b" fontSize={12} tickFormatter={(val) => `${val}y`} />
        <YAxis dataKey="organ" type="category" width={100} stroke="#334155" fontSize={11} fontWeight={500} />
        <Tooltip content={<ScientificTooltip />} cursor={{fill: '#f1f5f9'}} />
        <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
        <Bar dataKey="mae_linear" name="Linear MAE" fill="#cbd5e1" radius={[0, 4, 4, 0]} barSize={12} />
        <Bar dataKey="mae_nonlinear" name="Non-Linear MAE" fill="#334155" radius={[0, 4, 4, 0]} barSize={12} />
      </BarChart>
    </ResponsiveContainer>
  );
};

// -- Correlation Heatmap (Custom Implementation for simplicity) --
export const CorrelationHeatmap: React.FC<{ data: CorrelationMatrix }> = ({ data }) => {
  const getColor = (value: number) => {
    // Blue to Red gradient
    if (value === 1) return '#f1f5f9'; // Diagonal
    const intensity = Math.abs(value);
    // Simple red scale for positive, blue for negative (though data is mostly positive here)
    if (value > 0) return `rgba(225, 29, 72, ${intensity})`; // Red-ish
    return `rgba(71, 85, 105, ${intensity})`; 
  };

  return (
    <div className="grid grid-cols-6 gap-1 text-xs">
      <div className="col-span-1"></div>
      {data.labels.map((l, i) => (
        <div key={i} className="flex items-end justify-center font-medium text-slate-500 pb-2 rotate-45 origin-bottom-left translate-x-4">
          {l.replace('Metabolic', '')}
        </div>
      ))}
      
      {data.matrix.map((row, i) => (
        <React.Fragment key={i}>
          <div className="col-span-1 flex items-center justify-end pr-2 font-medium text-slate-500">
            {data.labels[i].replace('Metabolic', '')}
          </div>
          {row.map((val, j) => (
            <div 
              key={`${i}-${j}`}
              className="aspect-square flex items-center justify-center rounded-sm text-slate-700 transition-all hover:ring-2 ring-slate-300 relative group"
              style={{ backgroundColor: getColor(val) }}
            >
              {val !== 1 && val.toFixed(2)}
              {/* Tooltip on Hover */}
              <div className="absolute bottom-full mb-1 hidden group-hover:block bg-slate-800 text-white text-[10px] p-1 rounded whitespace-nowrap z-10">
                {data.labels[i]} vs {data.labels[j]}: {val.toFixed(3)}
              </div>
            </div>
          ))}
        </React.Fragment>
      ))}
    </div>
  );
};

// -- Distribution Plot (Simulated with BarChart for histogram feel) --
// In a real d3 app we'd use kernel density estimation. Here we bin data.
export const DistributionPlot: React.FC<{ individuals: Individual[], organ: string, color: string }> = ({ individuals, organ, color }) => {
  const getGap = (ind: Individual) => {
    switch(organ) {
      case 'Liver': return ind.liver_age_gap;
      case 'Kidney': return ind.kidney_age_gap;
      case 'Cardio': return ind.cardio_age_gap;
      case 'Immune': return ind.immune_age_gap;
      case 'Heme': return ind.heme_age_gap;
      default: return 0;
    }
  };

  // Binning
  const bins: Record<string, number> = {};
  for(let i=-20; i<=20; i+=2) {
    bins[i] = 0;
  }
  individuals.forEach(ind => {
    const gap = getGap(ind);
    const bin = Math.floor(gap / 2) * 2;
    if (bin >= -20 && bin <= 20) {
      bins[bin] = (bins[bin] || 0) + 1;
    }
  });

  const chartData = Object.keys(bins).map(k => ({ bin: parseInt(k), count: bins[k] })).sort((a,b) => a.bin - b.bin);

  return (
    <ResponsiveContainer width="100%" height={180}>
      <BarChart data={chartData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
        <XAxis dataKey="bin" tick={{fontSize: 10}} stroke="#94a3b8" />
        <YAxis tick={{fontSize: 10}} stroke="#94a3b8" />
        <Tooltip content={<ScientificTooltip />} />
        <Bar dataKey="count" fill={color} opacity={0.8} />
        {/* Zero Line Reference */}
        {/* Recharts ReferenceLine is sometimes buggy in strict mode, simulating with CSS or overlay is safer but ReferenceLine is standard */}
      </BarChart>
    </ResponsiveContainer>
  );
};
