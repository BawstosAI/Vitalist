
import { Individual, OrganMetric, ClusterInfo, FeatureImportance, CorrelationMatrix, AppData, AgeGapsResponse, ClustersResponse, FeatureImportanceResponse } from './types';

// --- MOCK DATA (Fallback) ---

export const MOCK_METRICS: OrganMetric[] = [
  { organ: 'Liver', mae_linear: 6.8, mae_nonlinear: 5.2, improvement_pct: 23.5, r2: 0.62 },
  { organ: 'Kidney', mae_linear: 7.2, mae_nonlinear: 5.4, improvement_pct: 25.0, r2: 0.58 },
  { organ: 'Cardio-Metabolic', mae_linear: 5.5, mae_nonlinear: 4.1, improvement_pct: 25.4, r2: 0.74 },
  { organ: 'Immune', mae_linear: 6.1, mae_nonlinear: 4.9, improvement_pct: 19.6, r2: 0.65 },
  { organ: 'Hematologic', mae_linear: 5.9, mae_nonlinear: 4.8, improvement_pct: 18.6, r2: 0.61 },
];

export const MOCK_CLUSTERS: ClusterInfo[] = [
  { id: 1, name: 'Healthy Agers', percentage: 35, description: "Consistent decelerated aging across all systems." },
  { id: 2, name: 'Cardio-Metabolic Risk', percentage: 28, description: "High acceleration in metabolic and liver markers." },
  { id: 3, name: 'Immune-Hematologic', percentage: 22, description: "Dysregulation in immune cell counts and anemia markers." },
  { id: 4, name: 'Uniform Accelerated', percentage: 15, description: "Systemic accelerated aging across >3 organs." },
];

export const MOCK_CORRELATIONS: CorrelationMatrix = {
  labels: ['Liver', 'Kidney', 'Cardio', 'Immune', 'Heme'],
  matrix: [
    [1.00, 0.35, 0.42, 0.15, 0.28],
    [0.35, 1.00, 0.58, 0.22, 0.31],
    [0.42, 0.58, 1.00, 0.30, 0.45],
    [0.15, 0.22, 0.30, 1.00, 0.38],
    [0.28, 0.31, 0.45, 0.38, 1.00],
  ]
};

export const MOCK_FEATURES: Record<string, FeatureImportance[]> = {
  liver: [
    { feature: 'LBXSASSI', importance: 0.25, description: 'AST (Aspartate Aminotransferase)' },
    { feature: 'LBXSAL', importance: 0.18, description: 'Albumin' },
    { feature: 'LBXSGTSI', importance: 0.15, description: 'GGT (Gamma-Glutamyl Transferase)' },
    { feature: 'LBXSATSI', importance: 0.12, description: 'ALT (Alanine Aminotransferase)' },
    { feature: 'LBXSTB', importance: 0.08, description: 'Total Bilirubin' },
  ],
  kidney: [
    { feature: 'LBXSCR', importance: 0.28, description: 'Serum Creatinine' },
    { feature: 'LBXSBU', importance: 0.22, description: 'Blood Urea Nitrogen' },
    { feature: 'URXUMA', importance: 0.18, description: 'Urine Albumin' },
    { feature: 'LBXSUA', importance: 0.14, description: 'Uric Acid' },
  ],
  cardio_metabolic: [],
  immune: [],
  hematologic: []
};

// Generate 531 mock individuals
const generateIndividuals = (): Individual[] => {
  const data: Individual[] = [];
  for (let i = 0; i < 531; i++) {
    const age = Math.floor(Math.random() * (80 - 18 + 1)) + 18;
    const sex = Math.random() > 0.5 ? 'M' : 'F';
    
    // Generate gaps with some correlation (simplified)
    const baseNoise = (Math.random() - 0.5) * 10;
    const lGap = baseNoise + (Math.random() - 0.5) * 10;
    const kGap = baseNoise + (Math.random() - 0.5) * 10;
    const cGap = baseNoise + (Math.random() - 0.5) * 8;
    const iGap = (Math.random() - 0.5) * 15;
    const hGap = (Math.random() - 0.5) * 12;

    const n_acc = [lGap, kGap, cGap, iGap, hGap].filter(g => g > 5).length;
    
    // Assign cluster roughly based on gaps
    let cluster = 1;
    if (n_acc >= 3) cluster = 4;
    else if (cGap > 5 && lGap > 3) cluster = 2;
    else if (iGap > 5 || hGap > 5) cluster = 3;

    data.push({
      seqn: `P${10000 + i}`,
      age,
      sex,
      liver_age_gap: parseFloat(lGap.toFixed(1)),
      liver_age_bio: parseFloat((age + lGap).toFixed(1)),
      kidney_age_gap: parseFloat(kGap.toFixed(1)),
      kidney_age_bio: parseFloat((age + kGap).toFixed(1)),
      cardio_age_gap: parseFloat(cGap.toFixed(1)),
      cardio_age_bio: parseFloat((age + cGap).toFixed(1)),
      immune_age_gap: parseFloat(iGap.toFixed(1)),
      immune_age_bio: parseFloat((age + iGap).toFixed(1)),
      heme_age_gap: parseFloat(hGap.toFixed(1)),
      heme_age_bio: parseFloat((age + hGap).toFixed(1)),
      cluster,
      n_accelerated: n_acc
    });
  }
  return data;
};

export const MOCK_INDIVIDUALS = generateIndividuals();


// --- DATA LOADER LOGIC ---

export async function loadProjectData(): Promise<Omit<AppData, 'loading'>> {
  try {
    console.log("Attempting to load static JSON data...");
    
    // Define the fetch promises
    const pMetrics = fetch('/data/metrics_summary.json');
    const pGaps = fetch('/data/age_gaps.json');
    const pCorr = fetch('/data/correlations.json');
    const pClusters = fetch('/data/clusters.json');
    
    // Wait for all main files
    const responses = await Promise.allSettled([pMetrics, pGaps, pCorr, pClusters]);
    
    // Check if critical files (gaps and metrics) are missing
    const metricsRes = responses[0];
    const gapsRes = responses[1];
    
    if (metricsRes.status === 'rejected' || !metricsRes.value.ok || 
        gapsRes.status === 'rejected' || !gapsRes.value.ok) {
      throw new Error("Critical data files not found, falling back to mocks.");
    }

    // Parse Data
    const metricsData = await metricsRes.value.json();
    const gapsData = await gapsRes.value.json() as AgeGapsResponse;
    
    // Optional data with defaults if missing
    let correlationsData = MOCK_CORRELATIONS;
    if (responses[2].status === 'fulfilled' && responses[2].value.ok) {
        correlationsData = await responses[2].value.json();
    }
    
    let clustersData = MOCK_CLUSTERS;
    if (responses[3].status === 'fulfilled' && responses[3].value.ok) {
        const rawData = await responses[3].value.json();
        // Handle both wrapped format { clusters: [...] } and raw array format [...]
        if (Array.isArray(rawData)) {
            clustersData = rawData as ClusterInfo[];
        } else if (rawData && 'clusters' in rawData && Array.isArray((rawData as ClustersResponse).clusters)) {
            clustersData = (rawData as ClustersResponse).clusters;
        }
    }

    // Try to load features for each organ (optional)
    const organs = ['liver', 'kidney', 'cardio_metabolic', 'immune', 'hematologic'];
    const featuresData: Record<string, FeatureImportance[]> = { ...MOCK_FEATURES };
    
    await Promise.all(organs.map(async (organ) => {
        try {
            const res = await fetch(`/data/feature_importance/${organ}.json`);
            if (res.ok) {
                const data = await res.json() as FeatureImportanceResponse;
                featuresData[organ] = data.features;
            }
        } catch (e) {
            // Ignore missing feature files
        }
    }));

    console.log("Successfully loaded static data.");

    return {
      metrics: metricsData,
      individuals: gapsData.data,
      correlations: correlationsData,
      clusters: clustersData,
      features: featuresData
    };

  } catch (error) {
    console.warn("Using Mock Data due to load error:", error);
    // Return Mocks
    return {
      metrics: MOCK_METRICS,
      individuals: MOCK_INDIVIDUALS,
      correlations: MOCK_CORRELATIONS,
      clusters: MOCK_CLUSTERS,
      features: MOCK_FEATURES
    };
  }
}
