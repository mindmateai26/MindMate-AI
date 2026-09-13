import numpy as np
import pandas as pd
import os

np.random.seed(42)
n_samples = 800

# 9 core indicators scored from 1 to 5:
# 1. mood_rating (1=Positive/Stable, 5=Severely Depressed/Low)
# 2. stress_level (1=Very Low, 5=Extreme)
# 3. sleep_quality (1=Excellent, 5=Severe Insomnia/Disturbed)
# 4. concentration_difficulty (1=None, 5=Severe Inability to Focus)
# 5. academic_work_pressure (1=Minimal, 5=Overwhelming)
# 6. social_withdrawal (1=Highly Connected, 5=Completely Isolated)
# 7. energy_level (1=High Energy, 5=Severe Fatigue/Exhaustion)
# 8. anxiety_frequency (1=Rarely/Never, 5=Constant/Panic)
# 9. daily_functioning_impact (1=No Impact, 5=Cannot Perform Routine Tasks)

records = []
for _ in range(n_samples):
    base_tendency = np.random.choice([1, 2, 3, 4], p=[0.28, 0.35, 0.24, 0.13])
    
    mood = np.clip(int(np.round(np.random.normal(base_tendency, 0.65))), 1, 5)
    stress = np.clip(int(np.round(np.random.normal(base_tendency, 0.70))), 1, 5)
    sleep = np.clip(int(np.round(np.random.normal(base_tendency, 0.75))), 1, 5)
    concentration = np.clip(int(np.round(np.random.normal(base_tendency, 0.65))), 1, 5)
    work_pressure = np.clip(int(np.round(np.random.normal(base_tendency, 0.80))), 1, 5)
    social = np.clip(int(np.round(np.random.normal(base_tendency, 0.70))), 1, 5)
    energy = np.clip(int(np.round(np.random.normal(base_tendency, 0.65))), 1, 5)
    anxiety = np.clip(int(np.round(np.random.normal(base_tendency, 0.75))), 1, 5)
    functioning = np.clip(int(np.round(np.random.normal(base_tendency, 0.60))), 1, 5)
    
    composite = (
        mood * 1.5 +
        stress * 1.3 +
        sleep * 1.1 +
        concentration * 1.0 +
        work_pressure * 1.1 +
        social * 1.1 +
        energy * 1.0 +
        anxiety * 1.4 +
        functioning * 1.5
    )
    
    if composite <= 18.5:
        category = "Low"
    elif composite <= 27.5:
        category = "Mild"
    elif composite <= 37.5:
        category = "Moderate"
    else:
        category = "High"
        
    records.append({
        "mood_rating": mood,
        "stress_level": stress,
        "sleep_quality": sleep,
        "concentration_difficulty": concentration,
        "academic_work_pressure": work_pressure,
        "social_withdrawal": social,
        "energy_level": energy,
        "anxiety_frequency": anxiety,
        "daily_functioning_impact": functioning,
        "composite_score": round(composite, 2),
        "risk_category": category
    })

df = pd.DataFrame(records)
output_dir = "C:/Users/ELCOT/.gemini/antigravity/scratch/mindmate_ai_v2/backend/data"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "sample_data.csv")
df.to_csv(csv_path, index=False)
print(f"Generated {len(df)} samples saved to {csv_path}")
print(df["risk_category"].value_counts())
