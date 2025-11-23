import requests
import json

try:
    # Fetch from localhost
    response = requests.get('http://localhost:3000/data/metrics_summary.json', timeout=2)
    if response.status_code == 200:
        data = response.json()
        immune = [x for x in data if 'Immune' in x.get('organ', '')]
        if immune:
            print("IMMUNE servi par localhost:3000:")
            print(f"  improvement_pct: {immune[0]['improvement_pct']}%")
            print(f"  r2: {immune[0]['r2']}")
        else:
            print("Immune not found in response")
    else:
        print(f"Error: HTTP {response.status_code}")
except Exception as e:
    print(f"Cannot connect to localhost: {e}")

# Also check file directly
print("\nIMMUNE dans le fichier:")
with open('frontend/longevity---organ-aging-analysis---vitalist/public/data/metrics_summary.json') as f:
    data = json.load(f)
    immune = [x for x in data if 'Immune' in x['organ']]
    print(f"  improvement_pct: {immune[0]['improvement_pct']}%")
    print(f"  r2: {immune[0]['r2']}")
