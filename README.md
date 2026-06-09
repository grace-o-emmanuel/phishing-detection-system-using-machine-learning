# Phishing Detection System Using Machine Learning

A machine learning-based phishing detection system that classifies URLs as **phishing** or **legitimate** using supervised learning algorithms. This project leverages the **Random Forest** classifier as the primary model, achieving an accuracy of **96.4%**, to combat the increasing threat of modern phishing attacks that often evade traditional blacklist-based systems.

## 🎯 Aim and Objectives

**Aim:** To develop an intelligent, adaptive phishing detection system using machine learning techniques.

**Objectives:**
1. Design a phishing detection system using the Random Forest machine learning algorithm.
2. Train and test the system using phishing and legitimate URL datasets from PhishTank, OpenPhish, and UCI repositories.
3. Evaluate the performance of the system using accuracy, precision, recall, and F1-score metrics.
4. Compare the machine learning model against other algorithms and traditional detection systems.

## 🧠 System Architecture

The system follows an Object-Oriented Analysis and Design Methodology (OOADM). The workflow is as follows:
`Input URL → Preprocessing → Feature Extraction (URL length, domain age, special characters, HTTPS status) → Random Forest Classification → Output (Phishing/Legitimate)`

Unlike traditional blacklist systems that cannot detect zero-day phishing attacks, this machine learning approach adapts to evolving phishing techniques by identifying deviations in website features.

## 📊 Performance Evaluation

Four supervised machine learning models were trained and evaluated. The **Random Forest** algorithm outperformed all others due to its robustness and ensemble learning capabilities:

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Logistic Regression | 89.5% | 88.2% | 87.6% | 87.9% |
| Support Vector Machine | 92.3% | 91.8% | 90.5% | 91.1% |
| Decision Tree | 90.7% | 89.9% | 89.2% | 89.5% |
| **Random Forest** | **96.4%** | **95.8%** | **95.2%** | **95.5%** |

*False Negative Rate:* 5% | *False Positive Rate:* 4%

## 📂 Project Structure

```text
├── data/                        # Dataset files (phishing_dataset.csv)
├── notebooks/                   # Jupyter notebook (full pipeline)
├── src/                         # Source code
│   ├── feature_extraction.py    # URL feature extraction
│   ├── train_model.py           # Model training & evaluation
│   ├── predict.py               # Single-URL classification CLI
│   └── utils.py                 # Helper utilities
├── models/                      # Saved trained models (.pkl)
├── results/                     # Evaluation outputs (confusion matrix, charts)
├── app/                         # Flask web interface
│   ├── app.py
│   └── templates/
├── requirements.txt
└── README.md
```

## ⚙️ Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/grace-o-emmanuel/phishing-detection-system-using-machine-learning.git
cd phishing-detection-system-using-machine-learning
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Run the Web Interface
Start the Flask application to use the graphical interface:
```bash
python app/app.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

### Train and Evaluate Models
To retrain the models and generate evaluation metrics/graphs:
```bash
python src/train_model.py
```
This script saves the best model to `models/random_forest_model.pkl`.

### Classify a Single URL (CLI)
Test a specific URL via the command line:
```bash
python src/predict.py "http://secure-bank-login.xyz@verify-user"
```

## 📊 Dataset

The dataset was compiled from three publicly available sources ensuring diversity and reliability:
- **[PhishTank](https://www.phishtank.org)**: Community-verified phishing URL submissions.
- **[OpenPhish](https://openphish.com)**: Autonomous phishing intelligence feed.
- **[UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/phishing+websites)**: Benchmark phishing websites dataset.

## 🛠️ Technologies
- **Python 3.x**
- **Scikit-learn** (Machine Learning framework)
- **Pandas / NumPy** (Data manipulation)
- **Matplotlib / Seaborn** (Visualisation)
- **Flask** (Web interface)
- **Jupyter Notebook** (Interactive development)

## 🔮 Future Scope
- Integration as a real-time web browser extension.
- Integration into email security systems and enterprise cybersecurity infrastructure.
- Exploration of deep learning architectures (CNN, LSTM) for detecting structural patterns in complex URLs.
