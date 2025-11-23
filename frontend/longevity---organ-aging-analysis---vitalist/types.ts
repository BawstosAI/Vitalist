
export type OrganId = 'liver' | 'kidney' | 'cardio_metabolic' | 'immune' | 'hematologic';

export interface OrganMetric {
  organ: string;
  mae_linear: number;
  mae_nonlinear: number;
  improvement_pct: number;
  r2: number;
}

export interface Individual {
  seqn: string;
  age: number;
  sex: 'M' | 'F';
  liver_age_bio: number;
  liver_age_gap: number;
  kidney_age_bio: number;
  kidney_age_gap: number;
  cardio_age_bio: number;
  cardio_age_gap: number;
  immune_age_bio: number;
  immune_age_gap: number;
  heme_age_bio: number;
  heme_age_gap: number;
  cluster: number;
  n_accelerated: number;
  // Optional fields that might come from raw data
  [key: string]: any;
}

// Wrapper for the age_gaps.json file
export interface AgeGapsResponse {
  metadata: {
    n_individuals: number;
    organs: string[];
    date_generated: string;
  };
  data: Individual[];
  summary_stats: Record<string, { mean: number; std: number; min: number; max: number }>;
}

export interface ClusterInfo {
  id: number;
  name: string;
  percentage: number;
  description: string;
  characteristics?: any;
}

export interface ClustersResponse {
  clusters: ClusterInfo[];
  embedding?: any[];
}

export interface FeatureImportance {
  feature: string;
  importance: number;
  description: string;
  display_name?: string;
  direction?: string;
}

export interface FeatureImportanceResponse {
  organ: string;
  model: string;
  features: FeatureImportance[];
}

export interface CorrelationMatrix {
  labels: string[];
  matrix: number[][];
}

export interface AppData {
  metrics: OrganMetric[];
  individuals: Individual[];
  clusters: ClusterInfo[];
  correlations: CorrelationMatrix;
  features: Record<string, FeatureImportance[]>;
  loading: boolean;
}
