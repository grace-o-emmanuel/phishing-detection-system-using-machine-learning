"""
feature_extraction.py
---------------------
Extract URL-level features for phishing detection.

This module provides two modes of operation:
1. **Batch mode** — enrich an existing dataset with additional computed features.
2. **Single-URL mode** — extract a feature vector from a raw URL string for
   real-time classification.

Features extracted (aligned with Chapter 3 — System Design):
    - URL length
    - Number of dots in the URL
    - Presence of IP address in the URL
    - Use of URL shortening service
    - Presence of '@' symbol
    - Presence of double-slash redirect ('//')
    - Prefix/suffix with dash ('-') in the domain
    - Number of subdomains
    - HTTPS token in the domain part
    - URL depth (number of '/' separators)
    - Presence of suspicious keywords
"""

import re
import numpy as np


# ── Known URL shortening domains ──────────────────────────────
SHORTENING_SERVICES = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly",
    "is.gd", "buff.ly", "j.mp", "rb.gy", "cutt.ly",
    "shorturl.at", "tiny.cc"
}

# ── Suspicious keywords commonly found in phishing URLs ──────
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account",
    "banking", "confirm", "password", "signin", "ebayisapi",
    "webscr", "suspend", "alert", "paypal", "support"
]


def _has_ip_address(url):
    """Check if the URL contains an IP address instead of a domain name."""
    ip_pattern = re.compile(
        r"(https?://)?(\d{1,3}\.){3}\d{1,3}"
    )
    return 1 if ip_pattern.search(url) else -1


def _url_length_category(url):
    """Categorise URL length: <54 → legitimate(1), 54-75 → suspicious(0), >75 → phishing(-1)."""
    length = len(url)
    if length < 54:
        return 1
    elif length <= 75:
        return 0
    else:
        return -1


def _has_shortening_service(url):
    """Check if the URL uses a known URL shortening service."""
    url_lower = url.lower()
    for service in SHORTENING_SERVICES:
        if service in url_lower:
            return -1
    return 1


def _has_at_symbol(url):
    """Check for '@' symbol in the URL (used to redirect)."""
    return -1 if "@" in url else 1


def _has_double_slash_redirect(url):
    """Check for '//' appearing after the protocol (position > 7)."""
    # Find '//' after the initial 'http://' or 'https://'
    position = url.find("//", 8)  # skip the protocol part
    return -1 if position >= 0 else 1


def _has_prefix_suffix(url):
    """Check if the domain contains a dash '-' (prefix-suffix attack)."""
    try:
        # Extract domain from URL
        domain = url.split("//")[-1].split("/")[0].split("@")[-1]
        return -1 if "-" in domain else 1
    except Exception:
        return -1


def _count_subdomains(url):
    """Count the number of subdomains. ≤1 → legitimate, 2 → suspicious, >2 → phishing."""
    try:
        domain = url.split("//")[-1].split("/")[0].split("@")[-1]
        # Remove port if present
        domain = domain.split(":")[0]
        dots = domain.count(".")
        if dots <= 1:
            return 1   # e.g., example.com
        elif dots == 2:
            return 0   # e.g., www.example.com
        else:
            return -1  # e.g., sub.www.example.com
    except Exception:
        return -1


def _has_https_token(url):
    """Check if 'https' appears in the domain part (not protocol) — deception tactic."""
    try:
        domain = url.split("//")[-1].split("/")[0]
        return -1 if "https" in domain.lower() else 1
    except Exception:
        return -1


def _url_depth(url):
    """Count the depth of the URL path (number of '/' after the domain)."""
    try:
        path = url.split("//")[-1]
        depth = path.count("/")
        if depth <= 1:
            return 1
        elif depth <= 3:
            return 0
        else:
            return -1
    except Exception:
        return -1


def _count_special_chars(url):
    """Count suspicious special characters in the URL."""
    special = sum(1 for c in url if c in "~!#$%^&*()_+={}|[]\\:;'<>?,")
    if special == 0:
        return 1
    elif special <= 5:
        return 0
    else:
        return -1


def _has_suspicious_keywords(url):
    """Check for phishing-related keywords in the URL."""
    url_lower = url.lower()
    count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url_lower)
    if count == 0:
        return 1
    elif count <= 2:
        return 0
    else:
        return -1


def _dot_count(url):
    """Count dots in the URL. More dots → more suspicious."""
    dots = url.count(".")
    if dots <= 3:
        return 1
    elif dots <= 5:
        return 0
    else:
        return -1


def extract_features_from_url(url):
    """
    Extract a feature vector from a single URL string.

    Parameters
    ----------
    url : str
        The raw URL to analyse.

    Returns
    -------
    list
        A list of numerical feature values (each -1, 0, or 1).
    """
    features = [
        _has_ip_address(url),
        _url_length_category(url),
        _has_shortening_service(url),
        _has_at_symbol(url),
        _has_double_slash_redirect(url),
        _has_prefix_suffix(url),
        _count_subdomains(url),
        _has_https_token(url),
        _url_depth(url),
        _count_special_chars(url),
        _has_suspicious_keywords(url),
        _dot_count(url),
    ]
    return features


def get_feature_names():
    """Return the ordered list of feature names matching extract_features_from_url output."""
    return [
        "having_IP_Address",
        "URL_Length",
        "Shortining_Service",
        "having_At_Symbol",
        "double_slash_redirecting",
        "Prefix_Suffix",
        "having_Sub_Domain",
        "HTTPS_token",
        "URL_Depth",
        "Special_Chars",
        "Suspicious_Keywords",
        "Dot_Count",
    ]


# ── CLI quick test ────────────────────────────────────────────
if __name__ == "__main__":
    test_urls = [
        "http://secure-bank-login.xyz@verify-user.com/account/confirm",
        "https://www.google.com",
        "http://192.168.1.1/login.php",
        "https://bit.ly/3xF9abc",
        "https://www.bank.com/login",
    ]

    names = get_feature_names()
    for url in test_urls:
        feats = extract_features_from_url(url)
        print(f"\nURL: {url}")
        for name, val in zip(names, feats):
            label = {1: "Legit", 0: "Suspicious", -1: "Phishing"}[val]
            print(f"  {name:30s} → {val:+d}  ({label})")
