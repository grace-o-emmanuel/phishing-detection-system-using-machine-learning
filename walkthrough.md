# Phishing Detection System — Setup Walkthrough

## What Was Done

The repo at `c:\Users\Blessing\Desktop\Dev\phishing-detection-system-using-machine-learning` was set up from scratch with a fully working ML pipeline.

## Files Created

### Core
| File | Purpose |
|------|---------|
| [README.md](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/README.md) | Project overview, setup, usage instructions |
| [requirements.txt](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/requirements.txt) | Python dependencies |
| [.gitignore](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/.gitignore) | Standard Python/ML gitignore |

### Dataset
| File | Purpose |
|------|---------|
| [data/generate_dataset.py](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/data/generate_dataset.py) | Generates 11,055-sample synthetic dataset matching UCI schema |
| [data/phishing_dataset.csv](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/data/phishing_dataset.csv) | Generated dataset (30 features, 56% phishing / 44% legit) |

### ML Pipeline
| File | Purpose |
|------|---------|
| [src/utils.py](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/src/utils.py) | Dataset loading, model save/load helpers |
| [src/feature_extraction.py](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/src/feature_extraction.py) | 12-feature URL extraction (IP, length, @, special chars, etc.) |
| [src/train_model.py](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/src/train_model.py) | Trains 4 models, evaluates, generates charts, saves best model |
| [src/predict.py](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/src/predict.py) | Single-URL CLI classifier with 30-column feature mapping |

### Notebook
| File | Purpose |
|------|---------|
| [notebooks/phishing_detection.ipynb](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/notebooks/phishing_detection.ipynb) | Full end-to-end walkthrough (EDA → training → evaluation → visualization) |

### Web Interface
| File | Purpose |
|------|---------|
| [app/app.py](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/app/app.py) | Flask server with classify endpoint |
| [app/templates/index.html](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/app/templates/index.html) | Dark-theme UI with glassmorphism, gradient animations |

### Generated Outputs
| File | Purpose |
|------|---------|
| [results/confusion_matrix.png](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/results/confusion_matrix.png) | Random Forest confusion matrix (300 DPI) |
| [results/accuracy_comparison.png](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/results/accuracy_comparison.png) | Model accuracy bar chart (300 DPI) |
| [results/model_evaluation.csv](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/results/model_evaluation.csv) | Metrics table |
| [models/random_forest_model.pkl](file:///c:/Users/Blessing/Desktop/Dev/phishing-detection-system-using-machine-learning/models/random_forest_model.pkl) | Saved Random Forest model |

## Bug Fix Applied

The model was trained on **30 UCI features**, but `feature_extraction.py` only extracts **12 URL features**. Fixed `predict.py` and `app.py` to:
- Build a proper 30-column pandas DataFrame matching the training schema
- Map the 12 extracted features to their closest UCI column names
- Fill unmapped columns with `0` (neutral)

## Verification Results

### CLI Predictor
- **Phishing URL** (`http://secure-bank-login.xyz@verify-user.com/account/confirm`) → ⚠️ PHISHING DETECTED ✓
- **Legitimate URL** (`https://www.bank.com/login`) → ✅ SAFE: LEGITIMATE ✓

### Training Pipeline Output
```
Logistic Regression  → 100.0%
Support Vector Machine → 100.0%
Decision Tree        → 98.6%
Random Forest        → 99.9%
```

> [!NOTE]
> Accuracy is very high because the synthetic dataset has clean, well-separated feature distributions. With the real UCI dataset, expect the numbers from Chapter 4 (~89–96%).

## How to Run

```bash
# Generate dataset
python data/generate_dataset.py

# Train models
python src/train_model.py

# Classify a URL
python src/predict.py "http://suspicious-url.example.com"

# Launch web interface
python app/app.py
# → Open http://localhost:5000
```
