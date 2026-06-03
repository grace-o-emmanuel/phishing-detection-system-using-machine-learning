# Phishing Detection System — Repository Setup

Set up a complete, working phishing detection project that matches the final year project report (Chapters 3–5).

## Proposed Changes

### Project Structure

```
phishing-detection-system-using-machine-learning/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── phishing_dataset.csv          # UCI phishing website dataset (30 features)
├── notebooks/
│   └── phishing_detection.ipynb      # Jupyter notebook — full pipeline
├── src/
│   ├── __init__.py
│   ├── feature_extraction.py         # URL feature extraction module
│   ├── train_model.py                # Train & evaluate all 4 models
│   ├── predict.py                    # Single-URL classification CLI
│   └── utils.py                      # Helpers (loading, saving, etc.)
├── models/
│   └── .gitkeep                      # Trained model artifacts (generated)
├── results/
│   └── .gitkeep                      # Evaluation outputs (generated)
└── app/
    ├── app.py                        # Flask web interface
    └── templates/
        └── index.html                # Simple URL input + result page
```

---

### 1. Core Files

#### [NEW] README.md
Project overview, setup instructions, usage guide, and attribution.

#### [NEW] requirements.txt
```
pandas
numpy
scikit-learn
matplotlib
seaborn
flask
jupyter
requests
python-whois
tldextract
beautifulsoup4
```

#### [NEW] .gitignore
Standard Python `.gitignore` — venv, `__pycache__`, `.ipynb_checkpoints`, `models/*.pkl`, etc.

---

### 2. Dataset (`data/`)

#### [NEW] data/phishing_dataset.csv
- Use the **UCI Phishing Websites** dataset (11,055 instances, 30 features, binary label).
- Download from UCI ML Repository or generate a synthetic version with matching schema if unavailable offline.
- Features include: `having_IP_Address`, `URL_Length`, `Shortining_Service`, `having_At_Symbol`, `double_slash_redirecting`, `Prefix_Suffix`, `having_Sub_Domain`, `SSLfinal_State`, `Domain_registeration_length`, `Favicon`, `port`, `HTTPS_token`, `Request_URL`, `URL_of_Anchor`, `Links_in_tags`, `SFH`, `Submitting_to_email`, `Abnormal_URL`, `Redirect`, `on_mouseover`, `RightClick`, `popUpWidnow`, `Iframe`, `age_of_domain`, `DNSRecord`, `web_traffic`, `Page_Rank`, `Google_Index`, `Links_pointing_to_page`, `Statistical_report`, `Result` (label: -1 phishing, 1 legitimate).

---

### 3. Training Pipeline (`src/`)

#### [NEW] src/feature_extraction.py
- Extract URL-level features: URL length, domain age, special characters count, HTTPS status, number of subdomains, presence of IP address, use of URL shortening services.
- Used for both training data augmentation and real-time single-URL classification.

#### [NEW] src/train_model.py
- Load dataset, split 80/20 (random_state=42).
- Train four models: Logistic Regression, SVM, Decision Tree, Random Forest (n_estimators=100).
- Evaluate each with accuracy, precision, recall, F1-score.
- Generate confusion matrix for Random Forest.
- Save the best model (Random Forest) as `models/random_forest_model.pkl`.
- Save evaluation results to `results/`.

#### [NEW] src/predict.py
- Load saved model.
- Accept a URL string, extract features, classify, print result.

#### [NEW] src/utils.py
- Helper functions for loading/saving models and datasets.

---

### 4. Jupyter Notebook (`notebooks/`)

#### [NEW] notebooks/phishing_detection.ipynb
- Full end-to-end walkthrough: data loading → EDA → feature extraction → model training → evaluation → comparison chart → confusion matrix visualization.
- Matches the narrative in Chapters 3 and 4.

---

### 5. Web Interface (`app/`)

#### [NEW] app/app.py
- Flask app: single route, accepts URL input via form POST, extracts features, classifies, returns result.

#### [NEW] app/templates/index.html
- Clean, modern single-page UI: URL input field, submit button, result display (phishing/legitimate with color coding).

---

## Open Questions

> [!IMPORTANT]
> **Dataset**: Should I download the real UCI dataset (requires internet), or generate a synthetic one with the same schema so everything runs offline immediately?

> [!NOTE]
> **Web interface**: The Flask app is a simple demo UI. If you'd prefer a more polished frontend or no web interface at all, let me know.

## Verification Plan

### Automated Tests
1. `pip install -r requirements.txt` — all dependencies install cleanly
2. `python src/train_model.py` — trains all 4 models, prints evaluation table
3. `python src/predict.py "http://secure-bank-login.xyz@verify-user"` — returns phishing result
4. `python -m flask --app app/app run` — web interface launches on localhost

### Manual Verification
- Confirm output metrics match Chapter 4 table values
- Confirm confusion matrix matches Figure 4.1
