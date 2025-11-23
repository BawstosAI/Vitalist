import pandas as pd
import json

# Correlations du notebook (depuis age_gaps.parquet)
df = pd.read_parquet('data/processed/age_gaps.parquet')
gap_cols = [col for col in df.columns if col.endswith('_age_gap') and col != 'max_age_gap']
corr_notebook = df[gap_cols].corr()

print("="*60)
print("CORRÉLATIONS NOTEBOOK 04")
print("="*60)
print("\nOrganes:", [col.replace('_age_gap', '') for col in gap_cols])
print("\nMatrice:")
print(corr_notebook.round(3))

# Correlations du frontend
corr_frontend = json.load(open('frontend/longevity---organ-aging-analysis---vitalist/public/data/correlations.json'))

print("\n" + "="*60)
print("CORRÉLATIONS FRONTEND")
print("="*60)
print("\nLabels:", corr_frontend['labels'])
print("\nMatrice (première ligne):")
print([round(x, 3) for x in corr_frontend['matrix'][0]])

print("\n" + "="*60)
print("COMPARAISON")
print("="*60)

# Compare first row (liver)
notebook_first = corr_notebook.iloc[0].values
frontend_first = corr_frontend['matrix'][0]

print("\nPremière ligne (Liver):")
print("Notebook:", [round(x, 3) for x in notebook_first])
print("Frontend:", [round(x, 3) for x in frontend_first])
print("Match:", all(abs(notebook_first[i] - frontend_first[i]) < 0.01 for i in range(len(notebook_first))))

# Summary stats from notebook
print("\n" + "="*60)
print("STATISTIQUES RÉSUMÉES (Notebook)")
print("="*60)
gap_summary = []
for col in gap_cols:
    organ = col.replace('_age_gap', '')
    gap_summary.append({
        'Organ': organ,
        'Mean': df[col].mean(),
        'Std': df[col].std(),
        'Min': df[col].min(),
        'Max': df[col].max()
    })
gap_df = pd.DataFrame(gap_summary)
print(gap_df.round(2))
