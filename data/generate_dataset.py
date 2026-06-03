"""
generate_dataset.py
-------------------
Generate a synthetic phishing dataset matching the UCI Phishing Websites
dataset schema (30 features + 1 label column).

This creates a realistic dataset for development and testing purposes.
The generated data mimics the statistical properties of the original
UCI dataset (11,055 instances, ~56% phishing, ~44% legitimate).

Run:
    python data/generate_dataset.py

Output:
    data/phishing_dataset.csv
"""

import os
import numpy as np
import pandas as pd

# ── Configuration ─────────────────────────────────────────────
NUM_SAMPLES = 11055
PHISHING_RATIO = 0.56  # ~56% phishing, 44% legitimate
RANDOM_STATE = 42

# ── Feature names (matching UCI Phishing Websites dataset) ────
FEATURE_NAMES = [
    "having_IP_Address",
    "URL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "SSLfinal_State",
    "Domain_registeration_length",
    "Favicon",
    "port",
    "HTTPS_token",
    "Request_URL",
    "URL_of_Anchor",
    "Links_in_tags",
    "SFH",
    "Submitting_to_email",
    "Abnormal_URL",
    "Redirect",
    "on_mouseover",
    "RightClick",
    "popUpWidnow",
    "Iframe",
    "age_of_domain",
    "DNSRecord",
    "web_traffic",
    "Page_Rank",
    "Google_Index",
    "Links_pointing_to_page",
    "Statistical_report",
]

LABEL_COL = "Result"


def generate_dataset():
    """Generate a synthetic phishing dataset."""
    np.random.seed(RANDOM_STATE)

    n_phishing = int(NUM_SAMPLES * PHISHING_RATIO)
    n_legitimate = NUM_SAMPLES - n_phishing

    data = {}

    # ── Phishing-biased features ──────────────────────────────
    # These features strongly correlate with phishing (-1)
    phishing_strong = [
        "having_IP_Address", "Shortining_Service", "having_At_Symbol",
        "double_slash_redirecting", "Prefix_Suffix", "HTTPS_token",
        "Submitting_to_email", "Abnormal_URL", "Iframe",
    ]

    for feat in FEATURE_NAMES:
        if feat in phishing_strong:
            # Phishing samples: ~80% chance of -1, 10% of 0, 10% of 1
            phish_vals = np.random.choice(
                [-1, 0, 1], size=n_phishing, p=[0.80, 0.10, 0.10]
            )
            # Legitimate samples: ~80% chance of 1, 10% of 0, 10% of -1
            legit_vals = np.random.choice(
                [-1, 0, 1], size=n_legitimate, p=[0.10, 0.10, 0.80]
            )
        elif feat in ["URL_Length", "having_Sub_Domain", "URL_of_Anchor",
                       "Links_in_tags", "SFH", "Request_URL"]:
            # Moderate correlation features
            phish_vals = np.random.choice(
                [-1, 0, 1], size=n_phishing, p=[0.65, 0.15, 0.20]
            )
            legit_vals = np.random.choice(
                [-1, 0, 1], size=n_legitimate, p=[0.15, 0.15, 0.70]
            )
        elif feat in ["SSLfinal_State", "Domain_registeration_length",
                       "age_of_domain", "DNSRecord", "Google_Index"]:
            # Important but less discriminative
            phish_vals = np.random.choice(
                [-1, 0, 1], size=n_phishing, p=[0.55, 0.20, 0.25]
            )
            legit_vals = np.random.choice(
                [-1, 0, 1], size=n_legitimate, p=[0.20, 0.15, 0.65]
            )
        elif feat in ["Redirect", "on_mouseover", "RightClick", "popUpWidnow"]:
            # Binary-like features (mostly 1 or -1)
            phish_vals = np.random.choice(
                [-1, 1], size=n_phishing, p=[0.60, 0.40]
            )
            legit_vals = np.random.choice(
                [-1, 1], size=n_legitimate, p=[0.15, 0.85]
            )
        else:
            # Weak features (web_traffic, Page_Rank, etc.)
            phish_vals = np.random.choice(
                [-1, 0, 1], size=n_phishing, p=[0.45, 0.25, 0.30]
            )
            legit_vals = np.random.choice(
                [-1, 0, 1], size=n_legitimate, p=[0.25, 0.20, 0.55]
            )

        data[feat] = np.concatenate([phish_vals, legit_vals])

    # ── Labels ────────────────────────────────────────────────
    data[LABEL_COL] = np.concatenate([
        np.full(n_phishing, -1),   # Phishing
        np.full(n_legitimate, 1),  # Legitimate
    ])

    # ── Shuffle ───────────────────────────────────────────────
    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

    # ── Save ──────────────────────────────────────────────────
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "phishing_dataset.csv")
    df.to_csv(output_path, index=False)

    print("=" * 55)
    print("  DATASET GENERATION COMPLETE")
    print("=" * 55)
    print(f"  Samples:    {len(df)}")
    print(f"  Features:   {len(FEATURE_NAMES)}")
    print(f"  Phishing:   {n_phishing} ({PHISHING_RATIO*100:.0f}%)")
    print(f"  Legitimate: {n_legitimate} ({(1-PHISHING_RATIO)*100:.0f}%)")
    print(f"  Saved to:   {output_path}")
    print("=" * 55)

    return df


if __name__ == "__main__":
    generate_dataset()
