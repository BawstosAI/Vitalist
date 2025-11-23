# Vitalist - Organ Aging Analysis Portal

Interactive web application for exploring biological aging patterns across human organ systems using NHANES data.

## Overview

Vitalist provides an intuitive interface to visualize and analyze organ-specific aging trajectories, biological age gaps, and aging phenotypes derived from machine learning models trained on NHANES biomarker data.

## Features

- **Dashboard**: Overview of aging metrics and key statistics
- **Performance**: Model performance metrics and validation results
- **Analysis**: Deep dive into organ age gaps and correlations
- **Phenotypes**: Clustering analysis of aging patterns
- **Explorer**: Interactive data exploration tools

## Run Locally

**Prerequisites:** Node.js (v18 or higher recommended)

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:5173](http://localhost:5173) in your browser

## Data Files

The application loads pre-computed analysis results from `/public/data/`:
- `age_gaps.json` - Biological age gaps for all individuals
- `metrics_summary.json` - Model performance metrics
- `correlations.json` - Cross-organ correlation matrices
- `clusters.json` - Aging phenotype cluster assignments
- `trajectories.json` - Age trajectory patterns
- `feature_importance/` - Feature importance for each organ system

## Technology Stack

- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **UI Components**: Radix UI
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Data Viz**: D3.js

## Project Structure

```
src/
├── components/     # React components
├── lib/           # Utility functions
├── data.ts        # Data loading logic
└── main.tsx       # Application entry point
public/
└── data/          # JSON data files
```
