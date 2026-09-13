import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "backend", "data", "sample_data.csv")
    models_dir = os.path.join(current_dir, "..", "backend", "models")
    os.makedirs(models_dir, exist_ok=True)
    model_output_path = os.path.join(models_dir, "prediction_model.joblib")

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    feature_cols = [
        "mood_rating",
        "stress_level",
        "sleep_quality",
        "concentration_difficulty",
        "academic_work_pressure",
        "social_withdrawal",
        "energy_level",
        "anxiety_frequency",
        "daily_functioning_impact"
    ]
    target_col = "risk_category"

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Training RandomForestClassifier on {len(X_train)} samples...")
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Test Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    importances = dict(zip(feature_cols, [round(float(v), 4) for v in clf.feature_importances_]))
    print("Feature Importances:")
    for k, v in sorted(importances.items(), key=lambda item: item[1], reverse=True):
        print(f"  - {k}: {v * 100:.1f}%")

    model_payload = {
        "model": clf,
        "feature_names": feature_cols,
        "classes": list(clf.classes_),
        "feature_importances": importances,
        "accuracy": round(float(acc), 4),
        "disclaimer": "This is a preliminary screening model for academic purposes and not a diagnostic medical device."
    }

    joblib.dump(model_payload, model_output_path)
    print(f"\nModel saved successfully to {model_output_path}")

if __name__ == "__main__":
    train()
