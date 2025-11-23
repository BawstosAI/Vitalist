# Organ-Specific Aging Analysis with NHANES

A machine learning framework for analyzing differential organ aging patterns using NHANES (National Health and Nutrition Examination Survey) data.

## 🎯 Project Overview

This project implements **organ clocks** - supervised ML models that predict chronological age from organ-specific biomarkers - to quantify biological aging at the organ level. By comparing predicted biological age with chronological age, we identify organs that are aging faster or slower than expected.

### Key Concepts

- **Organ Clock**: A machine learning model trained to predict age from organ-specific biomarkers
- **Biological Age**: The age predicted by an organ clock for a specific organ
- **Age Gap**: Difference between biological and chronological age (positive = accelerated aging)
- **Differential Aging**: Organs within the same individual age at different rates

### Why This Matters

- **Personalized Medicine**: Identify individual organ-specific health risks
- **Risk Stratification**: Go beyond chronological age for health assessment
- **Intervention Targeting**: Focus treatments on rapidly aging systems
- **Biological Understanding**: Uncover patterns in multi-organ aging

---

## 🏗️ Project Structure

```
Vitalist/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .gitignore                   # Git ignore rules
│
├── data/
│   ├── raw/                     # NHANES files (XPT/CSV) - not in repo
│   ├── interim/                 # Cleaned data
│   └── processed/               # Feature matrices and age gaps
│
├── configs/
│   ├── paths.yaml               # File paths configuration
│   └── organ_panels.yaml        # Organ biomarker definitions
│
├── notebooks/
│   ├── 00_overview_and_setup.ipynb
│   ├── 01_nhanes_data_preparation.ipynb
│   ├── 02_feature_engineering_organs.ipynb
│   ├── 03_train_organ_clocks.ipynb
│   ├── 04_analyze_agegaps.ipynb
│   ├── 05_trajectories_and_clustering.ipynb
│   └── 06_jury_storytelling_report.ipynb    # ⭐ Start here for overview
│
├── src/organ_aging/
│   ├── __init__.py
│   ├── config.py                # Configuration management
│   ├── data_loading.py          # NHANES data loading
│   ├── preprocessing.py         # Data cleaning
│   ├── features.py              # Feature engineering
│   ├── models.py                # Model training
│   ├── evaluation.py            # Performance metrics
│   ├── explainability.py        # SHAP, feature importance
│   ├── analysis.py              # Age gap analysis
│   ├── visualization.py         # Plotting functions
│   └── clustering.py            # PCA, UMAP, clustering
│
├── tests/                       # Unit tests (TDD approach)
│   ├── test_config.py
│   ├── test_data_loading.py
│   ├── test_preprocessing.py
│   ├── test_features.py
│   ├── test_models.py
│   ├── test_evaluation.py
│   ├── test_analysis.py
│   └── test_clustering.py
│
└── models/                      # Saved trained models
    ├── liver/
    ├── kidney/
    ├── cardio_metabolic/
    └── ...
```

---

## 🚀 Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd Vitalist

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Obtain NHANES Data

Download NHANES data files from [CDC NHANES website](https://wwwn.cdc.gov/nchs/nhanes/).

Required files (example from NHANES 2017-2018):
- `DEMO_J.XPT` - Demographics
- `BIOPRO_J.XPT` - Biochemistry profile
- `BPX_J.XPT` - Blood pressure
- `BMX_J.XPT` - Body measurements
- `TCHOL_J.XPT` - Cholesterol
- `GLU_J.XPT` - Glucose
- `ALB_CR_J.XPT` - Albumin & Creatinine
- `CBC_J.XPT` - Complete blood count
- `GHB_J.XPT` - Glycohemoglobin

Place all files in `data/raw/` directory.

### 3. Configure Paths

Edit `configs/paths.yaml` to match your downloaded NHANES files:

```yaml
raw_data_dir: "data/raw"

nhanes_files:
  demographics: "DEMO_J.XPT"     # Update with your file names
  biochemistry: "BIOPRO_J.XPT"
  # ... update other files
```

### 4. Configure Organ Panels

Edit `configs/organ_panels.yaml` to match NHANES variable names in your data cycle:

```yaml
liver:
  - LBXSATSI    # ALT
  - LBXSASSI    # AST
  # ... update variable names
```

**Important**: NHANES variable names vary by survey cycle. Consult the [NHANES documentation](https://wwwn.cdc.gov/nchs/nhanes/search/default.aspx) for your specific cycle.

### 5. Run Notebooks

Execute notebooks in order:

```bash
jupyter notebook
```

1. **00_overview_and_setup.ipynb** - Project introduction and verification
2. **01_nhanes_data_preparation.ipynb** - Load and clean data
3. **02_feature_engineering_organs.ipynb** - Build organ-specific datasets
4. **03_train_organ_clocks.ipynb** - Train ML models
5. **04_analyze_agegaps.ipynb** - Compute and analyze age gaps
6. **05_trajectories_and_clustering.ipynb** - Exploratory analysis
7. **06_jury_storytelling_report.ipynb** - ⭐ **Summary report for presentations**

---

## 🧬 Organ Systems Analyzed

| System | Biomarkers |
|--------|------------|
| **Liver** | ALT, AST, GGT, Alkaline Phosphatase, Albumin, Total Protein, Bilirubin |
| **Kidney** | Creatinine, BUN, Uric Acid, Urine Albumin, Albumin/Creatinine Ratio |
| **Cardio-Metabolic** | Blood Pressure, Total Cholesterol, HDL, LDL, Triglycerides, Glucose, HbA1c, BMI |
| **Immune** | White Blood Cell Count, Lymphocytes, Neutrophils, Monocytes, Eosinophils |
| **Hematologic** | Red Blood Cells, Hemoglobin, Hematocrit, MCV, MCHC, Platelets |

---

## 🤖 Machine Learning Approach

### Models

#### Baseline: Linear Models
- **ElasticNet** regression with L1+L2 regularization
- Interpretable coefficients
- Handles multicollinearity

#### Non-Linear Models
- **HistGradientBoosting** Regressor (scikit-learn)
- Alternative: XGBoost or LightGBM
- Captures non-linear aging patterns
- Built-in missing value handling

### Training Strategy

1. **Train/Val/Test Split**: 60% / 20% / 20%
2. **Stratification**: By age deciles to preserve age distribution
3. **Feature Scaling**: StandardScaler (fit on train only)
4. **Cross-Validation**: Optional 5-fold CV for robustness

### Evaluation Metrics

- **MAE** (Mean Absolute Error): Average prediction error in years
- **RMSE** (Root Mean Squared Error): Penalizes large errors
- **R²** (Coefficient of Determination): Proportion of variance explained

### Explainability

- **Feature Importance**: Coefficient magnitudes (linear) or gain (tree-based)
- **SHAP Values**: Marginal contribution of each biomarker to predictions
- **Permutation Importance**: Model-agnostic feature ranking

---

## 📊 Key Outputs

### 1. Model Performance
- Comparison of linear vs non-linear models
- Per-organ performance metrics
- Feature importance rankings

### 2. Age Gap Analysis
- Individual-level biological ages and gaps per organ
- Population distributions
- Correlation matrices between organs

### 3. Risk Stratification
- Identification of individuals with accelerated aging (gap > 5 years)
- Multi-organ acceleration patterns
- Co-occurrence analysis

### 4. Aging Phenotypes
- Clustering of individuals by aging profiles
- Distinct subtypes (e.g., "cardio-metabolic risk", "healthy agers")
- Demographic associations

### 5. Pseudo-Longitudinal Trajectories
- Age-binned trends in organ gaps
- Identification of organs that "break" first
- Cross-sectional approximation of aging dynamics

---

## 🧪 Testing (TDD Approach)

This project follows **Test-Driven Development** principles:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/organ_aging --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run tests with verbose output
pytest -v
```

Test coverage includes:
- ✅ Configuration loading
- ✅ Data loading and merging
- ✅ Preprocessing functions
- ✅ Feature engineering
- ✅ Model training and evaluation
- ✅ Age gap computation
- ✅ Analysis functions
- ✅ Clustering algorithms

---

## ⚠️ Limitations

### Cross-Sectional Data
NHANES is **cross-sectional** (snapshot in time), not longitudinal (tracking individuals over time).

**Implications**:
- We cannot observe true aging trajectories of individuals
- Age comparisons reflect different people, not the same person aging
- Cohort effects may confound age effects
- "Trajectories" are pseudo-longitudinal (age-binned averages)

### Biomarker Availability
- Limited to NHANES variables (no epigenetics, advanced imaging, proteomics)
- Variable names and availability vary by NHANES cycle
- Some organ systems have limited biomarkers

### Causality
- Models identify associations, not causal mechanisms
- Cannot determine if age gaps predict future health outcomes without longitudinal follow-up
- Confounding variables may influence results

### Generalizability
- NHANES is US-representative but may not generalize globally
- Results need validation in independent cohorts

---

## 📚 Scientific Background

### Key References

1. **Belsky et al. (2015).** "Quantification of biological aging in young adults." *PNAS*, 112(30).
   - Foundational work on measuring biological aging

2. **Horvath, S. (2013).** "DNA methylation age of human tissues and cell types." *Genome Biology*, 14(10).
   - Epigenetic aging clocks

3. **Levine et al. (2018).** "An epigenetic biomarker of aging for lifespan and healthspan." *Aging*, 10(4).
   - PhenoAge: phenotypic aging measure

4. **Jylhävä et al. (2017).** "Biological age predictors." *EBioMedicine*, 21.
   - Review of aging biomarkers

### Aging Biology Concepts

- **Hallmarks of Aging**: Genomic instability, telomere attrition, epigenetic alterations, loss of proteostasis, mitochondrial dysfunction, cellular senescence, stem cell exhaustion, altered intercellular communication, dysregulated nutrient sensing
- **Organ-Specific Aging**: Different tissues have varying stem cell pools, metabolic demands, and exposure to damage
- **Systemic vs Local Aging**: Some aging processes are systemic (inflammation, hormones), others are organ-specific

---

## 🎓 For Jury / Presentation

**Start with Notebook 06**: `06_jury_storytelling_report.ipynb`

This notebook provides:
- ✅ Executive summary of findings
- ✅ Key visualizations
- ✅ Model performance comparisons
- ✅ Example case studies
- ✅ Clinical implications
- ✅ Clear explanations of methodology

**Estimated review time**: 10-15 minutes

---

## 🛠️ Troubleshooting

### Missing NHANES Variables

If you get errors about missing columns:
1. Check your NHANES cycle documentation for variable names
2. Update `configs/organ_panels.yaml` with correct names
3. Use `df.columns` in notebook to see available variables

### Package Installation Issues

```bash
# If SHAP installation fails (requires compiler):
pip install shap --no-build-isolation

# If UMAP installation fails:
pip install umap-learn --no-deps
pip install pynndescent

# For Windows users with scikit-learn issues:
pip install --upgrade scikit-learn
```

### Memory Issues

For large NHANES datasets:
- Use Parquet format (more efficient than CSV)
- Process organs sequentially rather than all at once
- Reduce `background_samples` in SHAP calculations
- Use `dtype` optimization in pandas

---

## 🤝 Contributing

This project was developed for a hackathon/research competition. If extending:

1. **Add new organ systems**: Update `organ_panels.yaml`
2. **Test new models**: Modify `models.py` and add tests
3. **Enhance visualizations**: Extend `visualization.py`
4. **Add longitudinal data**: Adapt for cohorts with repeated measures

---

## 📄 License

This project is provided for educational and research purposes.

NHANES data is public domain (US government data).

---

## 📧 Contact

For questions about this project, please refer to the documentation in the notebooks or raise an issue in the repository.

---

## 🙏 Acknowledgments

- **NHANES**: CDC for providing comprehensive health survey data
- **Open Source Community**: scikit-learn, pandas, matplotlib, SHAP, UMAP
- **Aging Research Community**: For foundational work on biological aging

---

## ✅ Project Checklist

Before running:
- [ ] Downloaded NHANES data files
- [ ] Placed files in `data/raw/`
- [ ] Updated `configs/paths.yaml` with file names
- [ ] Updated `configs/organ_panels.yaml` with variable names
- [ ] Installed all requirements (`pip install -r requirements.txt`)
- [ ] Verified setup with `00_overview_and_setup.ipynb`

For presentation:
- [ ] Ran notebooks 01-05 to generate results
- [ ] Reviewed `06_jury_storytelling_report.ipynb`
- [ ] Prepared key visualizations
- [ ] Ready to explain limitations and future directions

---

**Happy Aging Analysis!** 🧬📊🤖
