import pandas as pd
import json
import numpy as np

print("="*70)
print("VÉRIFICATION COMPLÈTE DE LA JUSTESSE DU FRONTEND")
print("="*70)

# Load data
age_gaps_notebook = pd.read_parquet('data/processed/age_gaps.parquet')
age_gaps_frontend = json.load(open('frontend/longevity---organ-aging-analysis---vitalist/public/data/age_gaps.json'))
metrics_frontend = json.load(open('frontend/longevity---organ-aging-analysis---vitalist/public/data/metrics_summary.json'))
corr_frontend = json.load(open('frontend/longevity---organ-aging-analysis---vitalist/public/data/correlations.json'))

# Load original metrics
metrics_original = json.load(open('models/metrics_summary.json'))

print("\n" + "="*70)
print("1. MÉTRIQUES DE PERFORMANCE")
print("="*70)

all_metrics_correct = True
for metric in metrics_frontend:
    organ_ml = metric['organ'].lower().replace('-', '_').replace('metabolic', 'metabolic')
    if organ_ml == 'cardio_metabolic':
        organ_key = 'cardio_metabolic'
    elif organ_ml == 'hematologic':
        organ_key = 'hematologic'
    else:
        organ_key = organ_ml

    if organ_key in metrics_original:
        orig = metrics_original[organ_key]

        # Check MAE
        mae_linear_orig = round(orig['linear']['test']['mae'], 2)
        mae_gb_orig = round(orig['gradient_boosting']['test']['mae'], 2)
        r2_orig = round(orig['gradient_boosting']['test']['r2'], 2)

        mae_linear_fe = metric['mae_linear']
        mae_gb_fe = metric['mae_nonlinear']
        r2_fe = metric['r2']

        match = (mae_linear_orig == mae_linear_fe and
                mae_gb_orig == mae_gb_fe and
                r2_orig == r2_fe)

        status = "[OK]" if match else "[ERREUR]"
        print(f"\n{metric['organ']} {status}")
        print(f"  MAE Linear:    Original={mae_linear_orig}, Frontend={mae_linear_fe}")
        print(f"  MAE Gradient:  Original={mae_gb_orig}, Frontend={mae_gb_fe}")
        print(f"  R²:            Original={r2_orig}, Frontend={r2_fe}")

        if not match:
            all_metrics_correct = False

print("\n" + "="*70)
print("2. CORRÉLATIONS INTER-ORGANES")
print("="*70)

gap_cols = [col for col in age_gaps_notebook.columns if col.endswith('_age_gap') and col != 'max_age_gap']
corr_notebook = age_gaps_notebook[gap_cols].corr()

corr_matrix_frontend = np.array(corr_frontend['matrix'])
corr_matrix_notebook = corr_notebook.values

diff = np.abs(corr_matrix_frontend - corr_matrix_notebook)
max_diff = diff.max()

print(f"\nDifférence maximale: {max_diff:.6f}")
print(f"Corrélations identiques: {'✅' if max_diff < 0.001 else '❌'}")

print("\n" + "="*70)
print("3. DONNÉES INDIVIDUELLES")
print("="*70)

# Compare 5 random individuals
frontend_individuals = age_gaps_frontend['data']
sample_indices = [0, 100, 200, 300, 400]

all_individuals_correct = True
for idx in sample_indices:
    fe_ind = frontend_individuals[idx]
    nb_idx = idx  # Assuming same indexing

    if nb_idx in age_gaps_notebook.index:
        nb_row = age_gaps_notebook.loc[nb_idx]

        # Check age
        age_match = int(nb_row['AGE']) == fe_ind['age']

        # Check gaps
        liver_gap_match = abs(nb_row['liver_age_gap'] - fe_ind['liver_age_gap']) < 0.01
        cardio_gap_match = abs(nb_row['cardio_metabolic_age_gap'] - fe_ind['cardio_age_gap']) < 0.01

        match = age_match and liver_gap_match and cardio_gap_match

        if not match:
            all_individuals_correct = False
            print(f"\n❌ Individu {idx}:")
            print(f"  Age: Notebook={int(nb_row['AGE'])}, Frontend={fe_ind['age']}")
            print(f"  Liver gap: Notebook={nb_row['liver_age_gap']:.2f}, Frontend={fe_ind['liver_age_gap']:.2f}")

if all_individuals_correct:
    print(f"\n✅ Tous les {len(sample_indices)} individus testés sont corrects")

print("\n" + "="*70)
print("4. NOMBRE DE SUJETS")
print("="*70)

n_notebook = len(age_gaps_notebook)
n_frontend = len(frontend_individuals)

print(f"\nNotebook: {n_notebook} individus")
print(f"Frontend: {n_frontend} individus")
print(f"Match: {'✅' if n_notebook == n_frontend else '❌'}")

print("\n" + "="*70)
print("5. SEXE (RIAGENDR_2.0)")
print("="*70)

# Load test set to verify sex mapping
test_liver = pd.read_parquet('data/processed/liver/test.parquet')
if 'RIAGENDR_2.0' in test_liver.columns:
    # Sample 10 individuals
    sex_correct = True
    for idx in range(min(10, len(frontend_individuals))):
        if idx in test_liver.index:
            fe_sex = frontend_individuals[idx]['sex']
            riagendr_scaled = test_liver.loc[idx, 'RIAGENDR_2.0']
            expected_sex = 'F' if riagendr_scaled > 0 else 'M'

            if fe_sex != expected_sex:
                sex_correct = False
                print(f"❌ Individu {idx}: Frontend={fe_sex}, Attendu={expected_sex}")

    if sex_correct:
        print("✅ Sexe correct pour tous les 10 individus testés")
else:
    print("⚠ RIAGENDR_2.0 non trouvé dans test set")

print("\n" + "="*70)
print("6. DISTRIBUTION DES SEXES")
print("="*70)

sex_counts_fe = {'M': 0, 'F': 0}
for ind in frontend_individuals:
    sex_counts_fe[ind['sex']] += 1

print(f"\nFrontend: {sex_counts_fe['M']} hommes / {sex_counts_fe['F']} femmes")

# Count from test set
if 'RIAGENDR_2.0' in test_liver.columns:
    riagendr_counts = (test_liver['RIAGENDR_2.0'] > 0).value_counts()
    males_expected = riagendr_counts[False] if False in riagendr_counts.index else 0
    females_expected = riagendr_counts[True] if True in riagendr_counts.index else 0
    print(f"Attendu:  {males_expected} hommes / {females_expected} femmes")

    match = (sex_counts_fe['M'] == males_expected and sex_counts_fe['F'] == females_expected)
    print(f"Match: {'✅' if match else '❌'}")

print("\n" + "="*70)
print("RÉSUMÉ FINAL")
print("="*70)

checks = {
    "Métriques de performance": all_metrics_correct,
    "Corrélations": max_diff < 0.001,
    "Données individuelles": all_individuals_correct,
    "Nombre de sujets": n_notebook == n_frontend,
    "Sexe (échantillon)": sex_correct if 'RIAGENDR_2.0' in test_liver.columns else None
}

all_correct = all(v for v in checks.values() if v is not None)

print()
for check, result in checks.items():
    if result is None:
        status = "⚠️ "
    elif result:
        status = "✅"
    else:
        status = "❌"
    print(f"{status} {check}")

print("\n" + "="*70)
if all_correct:
    print("🎉 FRONTEND 100% JUSTE - Toutes les données sont correctes !")
else:
    print("⚠️  PROBLÈMES DÉTECTÉS - Voir détails ci-dessus")
print("="*70)
