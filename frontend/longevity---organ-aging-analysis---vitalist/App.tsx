
import React, { useState, useEffect } from 'react';
import { SectionHeader, Card, Badge, OrganLegendItem } from './components/ui';
import { PerformanceChart, CorrelationHeatmap, DistributionPlot } from './components/AnalysisCharts';
import { loadProjectData } from './data';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts';
import { OrganId, Individual, AppData, OrganMetric, ClusterInfo, FeatureImportance, CorrelationMatrix } from './types';

// Icons
const Icons = {
  Home: () => <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>,
  Chart: () => <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>,
  Users: () => <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>,
  Search: () => <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>,
  Dna: () => <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
};

// --- PAGES ---

interface PageProps {
  data: Omit<AppData, 'loading'>;
}

const Dashboard: React.FC<PageProps> = ({ data }) => {
  const { individuals, metrics } = data;
  const avgR2 = metrics.reduce((acc, m) => acc + m.r2, 0) / metrics.length;
  const multiAccelerated = individuals.filter(i => i.n_accelerated > 1).length;
  const pctMulti = ((multiAccelerated / individuals.length) * 100).toFixed(0);

  return (
    <div className="space-y-6">
      <SectionHeader title="Executive Summary" subtitle={`Vitalist analyzes differential organ aging using machine learning models trained on NHANES data. The test dataset contains ${individuals.length} persons.`} />
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Individuals Analyzed", val: individuals.length.toString(), sub: "Test Dataset" },
          { label: "Systems Modeled", val: metrics.length.toString(), sub: "Liver, Kidney, Cardio, Immune, Heme" },
          { label: "Avg Model R²", val: avgR2.toFixed(2), sub: "Across all organ clocks" },
          { label: "Multi-Organ Acceleration", val: `${pctMulti}%`, sub: ">1 organ with gap > 5y" },
        ].map((stat, i) => (
          <Card key={i} className="flex flex-col justify-between h-32 border-l-4 border-l-slate-400">
            <span className="text-slate-500 text-sm font-medium uppercase tracking-wider">{stat.label}</span>
            <div>
              <span className="text-4xl font-bold text-slate-800">{stat.val}</span>
              <p className="text-xs text-slate-400 mt-1">{stat.sub}</p>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Key Findings" className="h-full">
          <ul className="space-y-4">
            {[
              "Biological age deviates significantly from chronological age across all 5 systems.",
              "Organ systems aging often co-occur.",
              "Non-linear models (Gradient Boosting) not always outperform linear baselines.",
              "Distinct aging phenotypes were identified, clustering into 3 main groups."
            ].map((item, i) => (
              <li key={i} className="flex items-start gap-3 text-slate-700 text-sm">
                <span className="bg-slate-100 text-slate-500 font-mono text-xs px-1.5 py-0.5 rounded mt-0.5">{i+1}</span>
                {item}
              </li>
            ))}
          </ul>
        </Card>
        <Card title="Methodology Summary" className="h-full">
           <div className="flex flex-col h-full justify-center">
              <div className="flex items-center justify-between text-xs text-slate-500 mb-2 uppercase tracking-wide">
                <span>Data Input</span>
                <span>Processing</span>
                <span>Output</span>
              </div>
              <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden flex mb-4">
                 <div className="h-full bg-slate-300 w-1/3 border-r border-white"></div>
                 <div className="h-full bg-slate-400 w-1/3 border-r border-white"></div>
                 <div className="h-full bg-slate-600 w-1/3"></div>
              </div>
              <p className="text-sm text-slate-600 leading-relaxed">
                We utilized <strong>ElasticNet</strong> and <strong>HistGradientBoosting</strong> regressors to predict chronological age from organ-specific biomarkers. 
                The residual (Predicted - Actual) defines the <strong>Age Gap</strong>. Positive gaps indicate accelerated biological aging.
              </p>
           </div>
        </Card>
      </div>
    </div>
  );
};

const Performance: React.FC<PageProps> = ({ data }) => {
  return (
    <div className="space-y-6">
      <SectionHeader title="Model Performance" subtitle="Comparison of Linear vs Non-Linear regression models for Organ Clock construction." />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card title="Mean Absolute Error (MAE) Comparison">
            <PerformanceChart data={data.metrics} />
            <p className="text-xs text-slate-400 mt-4 text-center italic">A mean offset (e.g., 10 years) can be interpreted in two ways: either the clock imperfectly reflects the organ’s expected alignment with chronological age, or—conversely—it accurately captures that this organ tends to age about 10 years ahead of (or behind) the individual.</p>
          </Card>
        </div>
        <div>
          <Card title="Performance Metrics" className="h-full">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left text-slate-600">
                <thead className="text-xs text-slate-700 uppercase bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-3 py-2">Organ</th>
                    <th className="px-3 py-2 text-right">Imp. %</th>
                    <th className="px-3 py-2 text-right">R²</th>
                  </tr>
                </thead>
                <tbody>
                  {data.metrics.map((m) => (
                    <tr key={m.organ} className="border-b border-slate-100 hover:bg-slate-50">
                      <td className="px-3 py-2 font-medium">{m.organ}</td>
                      <td className={`px-3 py-2 text-right ${m.improvement_pct >= 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                        {m.improvement_pct >= 0 ? '+' : ''}{m.improvement_pct.toFixed(1)}%
                      </td>
                      <td className="px-3 py-2 text-right font-mono text-xs">{m.r2.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

const Analysis: React.FC<PageProps> = ({ data }) => {
  const { individuals, correlations } = data;
  
  return (
    <div className="space-y-8">
      <SectionHeader title="Age Gap Analysis" subtitle={`Distribution and correlation of biological aging acceleration across ${individuals.length} individuals.`} />
      
      {/* Distributions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[
          { key: 'Liver', color: '#d97706' },
          { key: 'Kidney', color: '#0d9488' },
          { key: 'Cardio', color: '#e11d48' },
          { key: 'Immune', color: '#9333ea' },
          { key: 'Heme', color: '#4f46e5' },
        ].map(o => (
          <Card key={o.key} title={`${o.key} Gap Distribution`}>
            <DistributionPlot individuals={individuals} organ={o.key} color={o.color} />
          </Card>
        ))}
        
        <Card title="Inter-Organ Correlations">
          <div className="h-[180px] flex items-center justify-center">
             <CorrelationHeatmap data={correlations} />
          </div>
        </Card>
      </div>

      <Card title="Accelerated Aging Prevalence">
        <div className="h-64 w-full">
            <ResponsiveContainer>
                <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis type="number" dataKey="age" name="Age" label={{ value: 'Chronological Age', position: 'bottom', offset: 0, fontSize: 12 }} stroke="#94a3b8" fontSize={12} domain={[18, 80]} />
                    <YAxis type="number" dataKey="n_accelerated" name="Accelerated Organs" label={{ value: '# Accelerated Organs (>5y)', angle: -90, position: 'insideLeft', fontSize: 12 }} stroke="#94a3b8" fontSize={12} allowDecimals={false} />
                    <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} content={({active, payload}) => {
                         if(active && payload && payload.length) {
                             return <div className="bg-white border p-2 text-xs shadow-sm rounded">
                                 Age: {payload[0].payload.age}<br/>
                                 Accelerated Systems: {payload[0].payload.n_accelerated}
                             </div>
                         }
                         return null;
                    }} />
                    <Scatter name="Individuals" data={individuals} fill="#8884d8">
                        {individuals.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.n_accelerated > 2 ? '#e11d48' : entry.n_accelerated > 0 ? '#64748b' : '#cbd5e1'} />
                        ))}
                    </Scatter>
                </ScatterChart>
            </ResponsiveContainer>
        </div>
        <div className="flex justify-center gap-4 mt-2">
            <OrganLegendItem color="#e11d48" label="High Risk (>2 organs)" />
            <OrganLegendItem color="#64748b" label="Moderate Risk (1-2 organs)" />
            <OrganLegendItem color="#cbd5e1" label="Low Risk (0 organs)" />
        </div>
      </Card>
    </div>
  );
};

const Phenotypes: React.FC<PageProps> = ({ data }) => {
    const { individuals, clusters } = data;

    // Cluster colors (matching K-means cluster IDs: 1, 2, 3)
    const getClusterColor = (id: number) => {
        const colors: Record<number, string> = {
            1: '#ef4444',  // red for Accelerated Young
            2: '#f59e0b',  // amber for Moderate Acceleration
            3: '#10b981'   // emerald for Balanced Seniors
        };
        return colors[id] || '#94a3b8';
    };

    return (
        <div className="space-y-6">
          <SectionHeader title="Aging Phenotypes" subtitle="K-means clustering (k=3) reveals distinct biological aging patterns from multi-organ analysis." />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {clusters.map(c => (
                <Card key={c.id} className="relative overflow-hidden">
                    <div className={`absolute top-0 left-0 w-1 h-full`} style={{ backgroundColor: getClusterColor(c.id) }}></div>
                    <div className="pl-2">
                        <div className="flex justify-between items-start mb-2">
                            <h3 className="font-bold text-slate-800">{c.name}</h3>
                            <span className="text-xs font-mono bg-slate-100 px-2 py-1 rounded text-slate-600">{c.percentage}%</span>
                        </div>
                        <p className="text-sm text-slate-500 leading-snug">{c.description}</p>
                        <div className="mt-3 flex items-center gap-2">
                            <span className="text-xs text-slate-400">Cluster {c.id}</span>
                            <span className="w-2 h-2 rounded-full" style={{ backgroundColor: getClusterColor(c.id) }}></span>
                        </div>
                    </div>
                </Card>
            ))}
          </div>

          <Card title="Cluster Distribution: Age vs Mean Organ Gap">
              <div className="h-[480px] w-full">
                 <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 70, left: 60 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                        <XAxis
                            type="number"
                            dataKey="age"
                            name="Age"
                            label={{ value: 'Chronological Age (years)', position: 'bottom', offset: 20, fontSize: 12, fill: '#64748b' }}
                            stroke="#94a3b8"
                            fontSize={11}
                            domain={[15, 85]}
                        />
                        <YAxis
                            type="number"
                            dataKey="meanGap"
                            name="Mean Gap"
                            label={{ value: 'Mean Age Gap (years)', angle: -90, position: 'insideLeft', offset: -40, fontSize: 12, fill: '#64748b' }}
                            stroke="#94a3b8"
                            fontSize={11}
                            domain={[-30, 30]}
                        />
                        <RechartsTooltip
                            cursor={{ strokeDasharray: '3 3' }}
                            content={({active, payload}) => {
                                if(active && payload && payload.length) {
                                    const p = payload[0].payload;
                                    const cluster = clusters.find(c => c.id === p.cluster);
                                    return <div className="bg-white border border-slate-200 p-3 text-xs shadow-lg rounded">
                                        <div className="font-bold text-slate-700 mb-1">{cluster?.name || `Cluster ${p.cluster}`}</div>
                                        <div>Age: {p.age} years</div>
                                        <div>Mean Gap: {p.meanGap.toFixed(1)} years</div>
                                        <div className="text-slate-400 mt-1">ID: {p.seqn}</div>
                                    </div>
                                }
                                return null;
                            }}
                        />
                        {[1, 2, 3].map(clusterId => (
                            <Scatter
                                key={clusterId}
                                name={clusters.find(c => c.id === clusterId)?.name || `Cluster ${clusterId}`}
                                data={individuals
                                    .filter(i => i.cluster === clusterId)
                                    .map(i => ({
                                        ...i,
                                        meanGap: (i.liver_age_gap + i.kidney_age_gap + i.cardio_age_gap + i.immune_age_gap + i.heme_age_gap) / 5
                                    }))
                                }
                                fill={getClusterColor(clusterId)}
                                fillOpacity={0.6}
                            />
                        ))}
                        <Legend
                            wrapperStyle={{ paddingTop: '20px' }}
                            iconType="circle"
                            verticalAlign="bottom"
                        />
                    </ScatterChart>
                 </ResponsiveContainer>
              </div>
              <p className="text-xs text-slate-400 mt-3 text-center">
                  Visualization of K-means clustering results. Each point represents an individual, colored by their aging phenotype.
                  Mean gap is the average biological age deviation across all 5 organ systems.
              </p>
          </Card>
        </div>
    );
};

const Explorer: React.FC<PageProps> = ({ data }) => {
    const { individuals } = data;
    const [selectedId, setSelectedId] = useState<string>('');
    const [search, setSearch] = useState("");
    
    // Set default on load
    useEffect(() => {
        if (individuals.length > 0 && !selectedId) {
            setSelectedId(individuals[0].seqn);
        }
    }, [individuals, selectedId]);
    
    const individual = individuals.find(i => i.seqn === selectedId) || individuals[0];
    
    if (!individual) return <div>No data available</div>;

    // Radar Data
    const radarData = [
        { subject: 'Liver', A: individual.liver_age_gap, fullMark: 15 },
        { subject: 'Kidney', A: individual.kidney_age_gap, fullMark: 15 },
        { subject: 'Cardio', A: individual.cardio_age_gap, fullMark: 15 },
        { subject: 'Immune', A: individual.immune_age_gap, fullMark: 15 },
        { subject: 'Heme', A: individual.heme_age_gap, fullMark: 15 },
    ];

    return (
        <div className="space-y-6">
            <SectionHeader title="Individual Explorer" subtitle="Inspect specific biological aging profiles." />
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="space-y-4">
                    <Card title="Select Individual">
                        <div className="flex gap-2 mb-4">
                            <input 
                                type="text" 
                                placeholder="Search ID..." 
                                className="w-full border border-slate-300 rounded-sm px-3 py-2 text-sm focus:outline-none focus:border-slate-500"
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                        </div>
                        <div className="h-96 overflow-y-auto border border-slate-100 rounded-sm">
                            {individuals.filter(i => i.seqn.toString().toLowerCase().includes(search.toLowerCase())).slice(0, 50).map(ind => (
                                <button 
                                    key={ind.seqn}
                                    onClick={() => setSelectedId(ind.seqn)}
                                    className={`w-full text-left px-4 py-3 text-sm border-b border-slate-50 flex justify-between items-center hover:bg-slate-50 ${selectedId === ind.seqn ? 'bg-slate-100 font-medium' : 'text-slate-600'}`}
                                >
                                    <span>{ind.seqn}</span>
                                    <span className={`text-xs px-1.5 py-0.5 rounded ${ind.n_accelerated > 1 ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-500'}`}>
                                        {ind.n_accelerated > 1 ? 'High Risk' : 'Normal'}
                                    </span>
                                </button>
                            ))}
                        </div>
                    </Card>
                </div>

                <div className="lg:col-span-2 space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                        <Card className="flex flex-col justify-center items-center py-8">
                             <span className="text-slate-500 text-xs uppercase tracking-widest mb-1">Chronological Age</span>
                             <span className="text-4xl font-bold text-slate-800">{individual.age}</span>
                             <span className="text-slate-400 text-sm">{individual.sex === 'M' ? 'Male' : 'Female'}</span>
                        </Card>
                        <Card className="flex flex-col justify-center items-center py-8">
                             <span className="text-slate-500 text-xs uppercase tracking-widest mb-1">Max Age Gap</span>
                             <span className={`text-4xl font-bold ${Math.max(individual.liver_age_gap, individual.kidney_age_gap, individual.cardio_age_gap) > 5 ? 'text-rose-600' : 'text-emerald-600'}`}>
                                {Math.max(individual.liver_age_gap, individual.kidney_age_gap, individual.cardio_age_gap, individual.immune_age_gap, individual.heme_age_gap).toFixed(1)}y
                             </span>
                             <span className="text-slate-400 text-sm">Worst performing organ</span>
                        </Card>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Card title="Aging Profile (Radar)">
                             <div className="h-[250px] w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                                        <PolarGrid stroke="#e2e8f0" />
                                        <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10, fill: '#64748b' }} />
                                        <PolarRadiusAxis angle={30} domain={[-10, 15]} tick={false} axisLine={false} />
                                        <Radar name={individual.seqn} dataKey="A" stroke="#475569" fill="#94a3b8" fillOpacity={0.4} />
                                    </RadarChart>
                                </ResponsiveContainer>
                             </div>
                        </Card>
                        <Card title="Organ Details">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="text-xs text-slate-500 border-b border-slate-100">
                                        <th className="text-left py-2">System</th>
                                        <th className="text-right py-2">Bio Age</th>
                                        <th className="text-right py-2">Gap</th>
                                    </tr>
                                </thead>
                                <tbody className="text-slate-700">
                                    {[
                                        { l: 'Liver', b: individual.liver_age_bio, g: individual.liver_age_gap },
                                        { l: 'Kidney', b: individual.kidney_age_bio, g: individual.kidney_age_gap },
                                        { l: 'Cardio', b: individual.cardio_age_bio, g: individual.cardio_age_gap },
                                        { l: 'Immune', b: individual.immune_age_bio, g: individual.immune_age_gap },
                                        { l: 'Heme', b: individual.heme_age_bio, g: individual.heme_age_gap },
                                    ].map(row => (
                                        <tr key={row.l} className="border-b border-slate-50">
                                            <td className="py-2">{row.l}</td>
                                            <td className="text-right py-2 text-slate-500">{row.b.toFixed(1)}</td>
                                            <td className="text-right py-2 font-mono">
                                                <span className={row.g > 3 ? 'text-rose-600 font-bold' : row.g < -3 ? 'text-emerald-600' : 'text-slate-600'}>
                                                    {row.g > 0 ? '+' : ''}{row.g.toFixed(1)}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}

// --- MAIN LAYOUT ---

export default function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [appData, setAppData] = useState<Omit<AppData, 'loading'> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
      async function init() {
          const data = await loadProjectData();
          setAppData(data);
          setLoading(false);
      }
      init();
  }, []);

  const navItems = [
    { id: 'dashboard', label: 'Executive Summary', icon: Icons.Home },
    { id: 'performance', label: 'Model Performance', icon: Icons.Chart },
    { id: 'analysis', label: 'Age Gap Analysis', icon: Icons.Dna },
    { id: 'phenotypes', label: 'Aging Phenotypes', icon: Icons.Users },
    { id: 'explorer', label: 'Individual Explorer', icon: Icons.Search },
  ];

  if (loading || !appData) {
      return (
          <div className="flex h-screen w-full items-center justify-center bg-slate-50">
              <div className="text-center">
                  <div className="w-10 h-10 border-4 border-slate-200 border-t-slate-800 rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-slate-500 text-sm font-medium">Loading Vitalist Data...</p>
                  <p className="text-slate-400 text-xs mt-1">Initializing static exports</p>
              </div>
          </div>
      );
  }

  return (
    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex-shrink-0 hidden md:flex flex-col z-20">
        <div className="p-6 border-b border-slate-100">
          <h1 className="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2">
            <span className="w-6 h-6 bg-slate-800 rounded-sm"></span>
            Vitalist
          </h1>
          <p className="text-xs text-slate-400 mt-1">Organ-Specific Aging Analysis</p>
        </div>
        
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium rounded-sm transition-colors ${
                currentView === item.id 
                  ? 'bg-slate-100 text-slate-900' 
                  : 'text-slate-500 hover:text-slate-800 hover:bg-slate-50'
              }`}
            >
              <item.icon />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-100">
          <div className="bg-slate-50 p-3 rounded-sm">
            <p className="text-xs font-semibold text-slate-700 mb-1">Project Status</p>
            <div className="flex items-center gap-2">
               <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
               <span className="text-xs text-slate-500">
                 {appData.individuals.length > 531 ? 'Live Data Loaded' : 'Static Export Loaded'}
               </span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative scroll-smooth">
        {/* Mobile Header */}
        <div className="md:hidden bg-white border-b border-slate-200 p-4 sticky top-0 z-10 flex justify-between items-center">
             <span className="font-bold text-slate-800">Vitalist</span>
             <select 
               value={currentView} 
               onChange={(e) => setCurrentView(e.target.value)}
               className="bg-slate-50 border border-slate-300 rounded px-2 py-1 text-sm"
             >
                {navItems.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}
             </select>
        </div>

        <div className="max-w-6xl mx-auto p-6 md:p-12 pb-24">
          {currentView === 'dashboard' && <Dashboard data={appData} />}
          {currentView === 'performance' && <Performance data={appData} />}
          {currentView === 'analysis' && <Analysis data={appData} />}
          {currentView === 'phenotypes' && <Phenotypes data={appData} />}
          {currentView === 'explorer' && <Explorer data={appData} />}
        </div>
        
        {/* Footer */}
        <footer className="border-t border-slate-200 bg-white py-6 px-6 md:px-12 text-center text-xs text-slate-400">
            Vitalist Project • NHANES 2017-2018 Data • Contributors : Blanche | Lucie | Bastien
        </footer>
      </main>
    </div>
  );
}
