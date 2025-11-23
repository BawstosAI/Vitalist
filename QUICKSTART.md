# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### Step 2: Verify Installation (1 min)

```bash
# Run tests to verify everything works
pytest tests/ -v

# Expected: 26 tests collected, most should pass
# Some may fail if optional packages (UMAP) not installed - that's OK
```

### Step 3: Get NHANES Data (2 min)

Download from: https://wwwn.cdc.gov/nchs/nhanes/

**Minimum required files** (example from 2017-2018 cycle):
- Demographics: `DEMO_J.XPT`
- Biochemistry: `BIOPRO_J.XPT`
- Blood Pressure: `BPX_J.XPT`
- Body Measures: `BMX_J.XPT`

Place all `.XPT` files in: `data/raw/`

### Step 4: Update Configuration (1 min)

Edit `configs/paths.yaml`:
```yaml
nhanes_files:
  demographics: "DEMO_J.XPT"     # ← Your file name
  biochemistry: "BIOPRO_J.XPT"   # ← Your file name
  # ... etc
```

Edit `configs/organ_panels.yaml`:
```yaml
liver:
  - LBXSATSI    # ← Check these match your NHANES cycle
  - LBXSASSI
  # ... etc
```

**How to find variable names:**
1. Go to https://wwwn.cdc.gov/nchs/nhanes/search/
2. Select your survey cycle
3. Search for components (e.g., "Biochemistry")
4. View variable list

### Step 5: Run Analysis

**Option A: Full Pipeline**
```bash
jupyter notebook
# Run notebooks 01 → 05 in order
```

**Option B: Quick Demo** (if you want to test without real data)
```python
# Open 00_overview_and_setup.ipynb
# This verifies your setup without needing data
```

---

## 📊 For Presentation / Jury

**→ Start with `notebooks/06_jury_storytelling_report.ipynb`**

This notebook provides:
- Executive summary
- Key findings
- Visualizations
- Model comparisons
- Clinical implications

**Estimated review time**: 10-15 minutes

---

## 🔍 Troubleshooting

### "Module not found" errors
```bash
# Install package
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### "Column not found" errors
- Update `configs/organ_panels.yaml` with correct NHANES variable names
- Variable names vary by NHANES cycle
- Use NHANES codebook to find correct names

### Tests failing for UMAP/SHAP
- These are optional packages
- Core functionality works without them
- Install if needed: `pip install umap-learn shap`

### Memory issues
- NHANES data can be large
- Process one organ at a time
- Use Parquet format instead of CSV

---

## 🎯 Expected Workflow

```
1. Setup (5 min)
   ↓
2. Run Notebook 01: Data Preparation (10 min)
   → Outputs: data/interim/nhanes_clean.parquet
   ↓
3. Run Notebook 02: Feature Engineering (5 min)
   → Outputs: data/processed/organ_datasets/
   ↓
4. Run Notebook 03: Train Models (15 min)
   → Outputs: models/[organ]/[model].pkl
   ↓
5. Run Notebook 04: Analyze Age Gaps (10 min)
   → Outputs: data/processed/age_gaps.parquet
   ↓
6. Run Notebook 05: Trajectories & Clustering (10 min)
   → Outputs: Visualizations and analysis
   ↓
7. Review Notebook 06: Presentation Report (5 min)
   → Key findings and visualizations
```

**Total Time**: ~1 hour for first run

---

## ✅ Success Checklist

Before running analysis:
- [ ] Installed all packages (`pip install -r requirements.txt`)
- [ ] Downloaded NHANES data files
- [ ] Placed files in `data/raw/`
- [ ] Updated `configs/paths.yaml` with file names
- [ ] Updated `configs/organ_panels.yaml` with variable names
- [ ] Ran tests (`pytest`) - most should pass
- [ ] Opened Jupyter (`jupyter notebook`)

Running analysis:
- [ ] Notebook 01 completed without errors
- [ ] Created `nhanes_clean.parquet`
- [ ] Notebook 02 created organ datasets
- [ ] Notebook 03 trained models successfully
- [ ] Notebook 04 computed age gaps
- [ ] Notebook 05 generated visualizations

For presentation:
- [ ] Reviewed Notebook 06 summary
- [ ] Identified key findings
- [ ] Prepared to explain limitations
- [ ] Ready to discuss future directions

---

## 🆘 Need Help?

1. **Check README.md** - Comprehensive documentation
2. **Review PROJECT_SUMMARY.md** - Project overview
3. **Run tests** - `pytest -v` shows what's working
4. **Check notebooks** - Each has detailed explanations
5. **NHANES documentation** - https://wwwn.cdc.gov/nchs/nhanes/

---

## 💡 Pro Tips

1. **Start small**: Test with 1-2 organs first
2. **Use Parquet**: Faster than CSV for large data
3. **Save intermediate outputs**: Don't re-run everything
4. **Check variable names**: Most common error source
5. **Read the markdown**: Notebooks have detailed explanations

---

**You're ready to go! Start with Notebook 01.** 🚀
