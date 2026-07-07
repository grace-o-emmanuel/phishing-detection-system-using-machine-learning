"""
predict.py
----------
Classify a single URL as phishing or legitimate using the trained
Random Forest model.

Usage:
    python src/predict.py "http://suspicious-url.example.com/login"
    python src/predict.py "https://www.google.com"
"""

import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_model
from src.feature_extraction import extract_features_from_url, get_feature_names, check_typosquatting

# ── The 30 UCI feature columns the model was trained on ───────
UCI_FEATURE_NAMES = [
    "having_IP_Address", "URL_Length", "Shortining_Service",
    "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix",
    "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length",
    "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor",
    "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL",
    "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe",
    "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank",
    "Google_Index", "Links_pointing_to_page", "Statistical_report",
]

# ── Mapping from extracted feature names → UCI column names ───
_FEATURE_MAP = {
    "having_IP_Address": "having_IP_Address",
    "URL_Length": "URL_Length",
    "Shortining_Service": "Shortining_Service",
    "having_At_Symbol": "having_At_Symbol",
    "double_slash_redirecting": "double_slash_redirecting",
    "Prefix_Suffix": "Prefix_Suffix",
    "having_Sub_Domain": "having_Sub_Domain",
    "HTTPS_token": "HTTPS_token",
    "URL_Depth": "Redirect",            # closest UCI proxy
    "Special_Chars": "Abnormal_URL",     # closest UCI proxy
    "Suspicious_Keywords": "SFH",        # closest UCI proxy
    "Dot_Count": "Links_in_tags",        # closest UCI proxy
}


def _build_feature_row(url):
    """
    Extract URL features and map them into a 30-column DataFrame row
    matching the UCI training schema.
    """
    raw_features = extract_features_from_url(url)
    raw_names = get_feature_names()

    # Start with all zeros (neutral)
    row = {col: 0 for col in UCI_FEATURE_NAMES}

    # Fill in the features we can extract
    for name, val in zip(raw_names, raw_features):
        uci_col = _FEATURE_MAP.get(name)
        if uci_col and uci_col in row:
            row[uci_col] = val

    return row, dict(zip(raw_names, raw_features))


def classify_url(url, model=None):
    """
    Classify a URL as phishing or legitimate.

    Parameters
    ----------
    url : str
        The URL to classify.
    model : object, optional
        A pre-loaded scikit-learn model. If None, loads the saved model.

    Returns
    -------
    dict
        Classification result with label and feature details.
    """
    if model is None:
        model = load_model()

    # Build a DataFrame row with all 30 UCI columns
    row, extracted_features = _build_feature_row(url)
    df = pd.DataFrame([row], columns=UCI_FEATURE_NAMES)

    # Predict
    prediction = model.predict(df)[0]

    # Check for typosquatting / brand-mimicking heuristic override
    is_typosquatted = check_typosquatting(url)

    # Determine label (UCI dataset: -1 = phishing, 1 = legitimate)
    is_phishing = int(prediction) == -1 or is_typosquatted

    if is_typosquatted:
        prediction = -1

    result = {
        "url": url,
        "prediction": int(prediction),
        "is_phishing": is_phishing,
        "label": "PHISHING" if is_phishing else "LEGITIMATE",
        "features": extracted_features,
    }

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python src/predict.py <URL>")
        print('Example: python src/predict.py "http://secure-bank-login.xyz@verify-user"')
        sys.exit(1)

    url = sys.argv[1]

    print("=" * 55)
    print("  PHISHING DETECTION SYSTEM")
    print("=" * 55)
    print(f"\n  Input URL: {url}\n")

    try:
        result = classify_url(url)
    except FileNotFoundError as e:
        print(f"  [ERROR] {e}")
        print("  Run 'python src/train_model.py' first to train the model.")
        sys.exit(1)

    if result["is_phishing"]:
        print("  ╔══════════════════════════════════════════╗")
        print("  ║  ⚠  WARNING: PHISHING WEBSITE DETECTED  ║")
        print("  ╚══════════════════════════════════════════╝")
    else:
        print("  ╔══════════════════════════════════════════╗")
        print("  ║  ✓  SAFE: LEGITIMATE WEBSITE             ║")
        print("  ╚══════════════════════════════════════════╝")

    print(f"\n  Classification: {result['label']}")
    print(f"  Raw prediction: {result['prediction']}")

    print("\n  Feature Analysis:")
    print("  " + "-" * 45)
    for name, val in result["features"].items():
        indicator = {1: "✓ Legit", 0: "? Suspicious", -1: "✗ Phishing"}[val]
        print(f"    {name:30s}  {val:+d}  {indicator}")
    print("  " + "-" * 45)

    print("\n" + "=" * 55)


if __name__ == "__main__":
    main()
