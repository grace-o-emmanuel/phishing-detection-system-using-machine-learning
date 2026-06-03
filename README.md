# Phishing Detection System Using Machine Learning

A machine learning-based phishing detection system that classifies URLs as **phishing** or **legitimate** using supervised learning algorithms. The **Random Forest** classifier is the primary model, achieving **96.4% accuracy**.

## Overview

This project implements and compares four supervised classification algorithms for URL-based phishing detection:

| Model               | Accuracy | Precision | Recall | F1-Score |
|----------------------|----------|-----------|--------|----------|
| Logistic Regression  | 89.5%    | 88.2%     | 87.6%  | 87.9%    |
| Support Vector Machine | 92.3% | 91.8%     | 90.5%  | 91.1%    |
| Decision Tree        | 90.7%    | 89.9%     | 89.2%  | 89.5%    |
| **Random Forest**    | **96.4%**| **95.8%** |**95.2%**|**95.5%**|

## Project Structure

```
├── data/                        # Dataset files
│   └── phishing_dataset.csv
├── notebooks/                   # Jupyter notebook (full pipeline)
│   └── phishing_detection.ipynb
├── src/                         # Source code
│   ├── feature_extraction.py    # URL feature extraction
│   ├── train_model.py           # Model training & evaluation
│   ├── predict.py               # Single-URL classification CLI
│   └── utils.py                 # Helper utilities
├── models/                      # Saved trained models (.pkl)
├── results/                     # Evaluation outputs
├── app/                         # Flask web interface
│   ├── app.py
│   └── templates/
│       └── index.html
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/grace-o-emmanuel/phishing-detection-system-using-machine-learning.git
cd phishing-detection-system-using-machine-learning
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Train and Evaluate Models

```bash
python src/train_model.py
```

This trains all four models, prints evaluation metrics, generates the confusion matrix, and saves the best model (Random Forest) to `models/random_forest_model.pkl`.

### Classify a Single URL (CLI)

```bash
python src/predict.py "http://secure-bank-login.xyz@verify-user"
```

### Run the Web Interface

```bash
python app/app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

### Jupyter Notebook

```bash
jupyter notebook notebooks/phishing_detection.ipynb
```

Full end-to-end walkthrough: data loading → EDA → feature extraction → model training → evaluation → visualisation.

## Dataset

The dataset used in this study was compiled from three publicly available sources:

- **[PhishTank](https://www.phishtank.org)** — community-verified phishing URL submissions
- **[OpenPhish](https://openphish.com)** — autonomous phishing intelligence feed
- **[UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/phishing+websites)** — benchmark phishing websites dataset (11,055 instances, 30 features)

## Technologies

- **Python 3.x** — core programming language
- **Scikit-learn** — model training and evaluation
- **Pandas / NumPy** — data manipulation and computation
- **Matplotlib / Seaborn** — visualisation
- **Flask** — web interface
- **Jupyter Notebook** — interactive development

## License

This project was developed as a final year research project.
