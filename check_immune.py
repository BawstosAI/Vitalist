import json

# Check frontend JSON
fe_metrics = json.load(open('frontend/longevity---organ-aging-analysis---vitalist/public/data/metrics_summary.json'))
immune_fe = [x for x in fe_metrics if 'Immune' in x['organ']][0]

print("IMMUNE dans le frontend JSON:")
print(f"  improvement_pct: {immune_fe['improvement_pct']}%")
print(f"  r2: {immune_fe['r2']}")
print(f"  mae_linear: {immune_fe['mae_linear']}")
print(f"  mae_nonlinear: {immune_fe['mae_nonlinear']}")

# Check original
orig_metrics = json.load(open('models/metrics_summary.json'))
immune_orig = orig_metrics['immune']

linear_mae = immune_orig['linear']['test']['mae']
gb_mae = immune_orig['gradient_boosting']['test']['mae']
gb_r2 = immune_orig['gradient_boosting']['test']['r2']
improvement = ((linear_mae - gb_mae) / linear_mae) * 100

print("\nIMMUNE dans models/ (original):")
print(f"  Linear MAE: {linear_mae:.2f}")
print(f"  GB MAE: {gb_mae:.2f}")
print(f"  GB R2: {gb_r2:.3f}")
print(f"  Improvement: {improvement:.1f}%")

print("\nCOMPARAISON:")
print(f"  Frontend improvement: {immune_fe['improvement_pct']}% vs Calculé: {improvement:.1f}%")
print(f"  Frontend R2: {immune_fe['r2']} vs Original: {round(gb_r2, 2)}")

if immune_fe['improvement_pct'] != round(improvement, 1):
    print("\nERREUR: Les valeurs ne correspondent pas!")
else:
    print("\nOK: Les valeurs correspondent")
