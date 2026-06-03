"""
train_model.py
--------------
Train and evaluate four supervised classification models for phishing URL
detection, as described in Chapter 4 of the project report.

Models:
    1. Logistic Regression
    2. Support Vector Machine (SVM)
    3. Decision Tree
    4. Random Forest (n_estimators=100)

Outputs:
    - Performance metrics table (Accuracy, Precision, Recall, F1-Score)
    - Confusion matrix for the Random Forest model
    - Model accuracy comparison bar chart
    - Saved Random Forest model (models/random_forest_model.pkl)
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving figures
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Add project root to path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import load_dataset, save_model, ensure_dirs, RESULTS_DIR


def train_and_evaluate():
    """Run the full training and evaluation pipeline."""

    ensure_dirs()

    # ── 1. Load dataset ───────────────────────────────────────
    print("=" * 60)
    print("  PHISHING DETECTION SYSTEM — MODEL TRAINING")
    print("=" * 60)

    df = load_dataset()

    # The UCI dataset uses 'Result' as the label column (-1 = phishing, 1 = legitimate)
    # Adapt to whatever column name is present
    label_col = None
    for candidate in ["Result", "result", "label", "Label", "class", "Class"]:
        if candidate in df.columns:
            label_col = candidate
            break

    if label_col is None:
        raise ValueError(
            "Could not find a label column in the dataset. "
            "Expected one of: Result, label, class."
        )

    X = df.drop(label_col, axis=1)
    y = df[label_col]

    # Ensure numeric features only
    X = X.select_dtypes(include=[np.number])

    print(f"[INFO] Features: {X.shape[1]}, Label column: '{label_col}'")
    print(f"[INFO] Class distribution:\n{y.value_counts().to_string()}\n")

    # ── 2. Split dataset (80/20) ──────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"[INFO] Training set: {X_train.shape[0]} samples")
    print(f"[INFO] Test set:     {X_test.shape[0]} samples\n")

    # ── 3. Define models ──────────────────────────────────────
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Support Vector Machine": SVC(kernel="rbf", random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    # ── 4. Train & evaluate each model ────────────────────────
    results = []

    for name, model in models.items():
        print(f"[TRAINING] {name}...", end=" ")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds) * 100
        prec = precision_score(y_test, preds, average="binary", pos_label=y.unique().max(), zero_division=0) * 100
        rec = recall_score(y_test, preds, average="binary", pos_label=y.unique().max(), zero_division=0) * 100
        f1 = f1_score(y_test, preds, average="binary", pos_label=y.unique().max(), zero_division=0) * 100

        results.append({
            "Model": name,
            "Accuracy (%)": round(acc, 1),
            "Precision (%)": round(prec, 1),
            "Recall (%)": round(rec, 1),
            "F1-Score (%)": round(f1, 1),
        })

        print(f"Accuracy: {acc:.1f}%")

    # ── 5. Display results table ──────────────────────────────
    results_df = pd.DataFrame(results)
    print("\n" + "=" * 60)
    print("  PERFORMANCE EVALUATION OF CLASSIFICATION MODELS")
    print("=" * 60)
    print(results_df.to_string(index=False))
    print("=" * 60)

    # Save results to CSV
    results_csv_path = os.path.join(RESULTS_DIR, "model_evaluation.csv")
    results_df.to_csv(results_csv_path, index=False)
    print(f"\n[INFO] Results saved to '{results_csv_path}'")

    # ── 6. Confusion matrix for Random Forest ─────────────────
    rf_model = models["Random Forest"]
    rf_preds = rf_model.predict(X_test)
    cm = confusion_matrix(y_test, rf_preds)

    print("\n" + "=" * 60)
    print("  CONFUSION MATRIX — RANDOM FOREST")
    print("=" * 60)
    print(f"  True Positives  : {cm[1][1] if cm.shape[0] > 1 else cm[0][0]}")
    print(f"  True Negatives  : {cm[0][0]}")
    print(f"  False Positives : {cm[0][1] if cm.shape[1] > 1 else 0}")
    print(f"  False Negatives : {cm[1][0] if cm.shape[0] > 1 else 0}")
    print("=" * 60)

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Phishing", "Legitimate"],
        yticklabels=["Phishing", "Legitimate"],
    )
    plt.title("Confusion Matrix — Random Forest Model", fontsize=14, fontweight="bold")
    plt.xlabel("Predicted", fontsize=12)
    plt.ylabel("Actual", fontsize=12)
    plt.tight_layout()

    cm_path = os.path.join(RESULTS_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[INFO] Confusion matrix saved to '{cm_path}'")

    # ── 7. Model accuracy comparison chart ────────────────────
    plt.figure(figsize=(10, 6))
    colors = ["#3498db", "#e74c3c", "#f39c12", "#2ecc71"]
    bars = plt.barh(
        results_df["Model"],
        results_df["Accuracy (%)"],
        color=colors,
        edgecolor="white",
        height=0.5,
    )

    # Add value labels on bars
    for bar, acc in zip(bars, results_df["Accuracy (%)"]):
        plt.text(
            bar.get_width() - 3,
            bar.get_y() + bar.get_height() / 2,
            f"{acc}%",
            va="center",
            ha="right",
            fontsize=12,
            fontweight="bold",
            color="white",
        )

    plt.xlabel("Accuracy (%)", fontsize=12)
    plt.title("Model Accuracy Comparison", fontsize=14, fontweight="bold")
    plt.xlim(80, 100)
    plt.tight_layout()

    chart_path = os.path.join(RESULTS_DIR, "accuracy_comparison.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"[INFO] Accuracy chart saved to '{chart_path}'")

    # ── 8. Save the best model (Random Forest) ────────────────
    save_model(rf_model)

    # ── 9. Full classification report ─────────────────────────
    print("\n" + "=" * 60)
    print("  DETAILED CLASSIFICATION REPORT — RANDOM FOREST")
    print("=" * 60)
    print(classification_report(y_test, rf_preds))

    print("\n[DONE] Training pipeline complete.")
    return results_df


if __name__ == "__main__":
    train_and_evaluate()
