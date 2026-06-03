"""
utils.py
--------
Helper utilities for loading datasets, saving/loading trained models,
and common path resolution used across the project.
"""

import os
import joblib
import pandas as pd


# ── Project root directory (two levels up from src/) ──────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Standard paths ────────────────────────────────────────────
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

DATASET_PATH = os.path.join(DATA_DIR, "phishing_dataset.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "random_forest_model.pkl")


def load_dataset(path=None):
    """
    Load the phishing dataset from CSV.

    Parameters
    ----------
    path : str, optional
        Custom path to the CSV file. Defaults to data/phishing_dataset.csv.

    Returns
    -------
    pd.DataFrame
        The loaded dataset.
    """
    if path is None:
        path = DATASET_PATH

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. "
            "Please place phishing_dataset.csv in the data/ directory."
        )

    df = pd.read_csv(path)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def save_model(model, path=None):
    """
    Save a trained model to disk using joblib.

    Parameters
    ----------
    model : object
        The trained scikit-learn model.
    path : str, optional
        Custom save path. Defaults to models/random_forest_model.pkl.
    """
    if path is None:
        path = MODEL_PATH

    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"[INFO] Model saved to '{path}'")


def load_model(path=None):
    """
    Load a trained model from disk.

    Parameters
    ----------
    path : str, optional
        Custom path to the model file. Defaults to models/random_forest_model.pkl.

    Returns
    -------
    object
        The loaded scikit-learn model.
    """
    if path is None:
        path = MODEL_PATH

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found at '{path}'. "
            "Run 'python src/train_model.py' first to train and save the model."
        )

    model = joblib.load(path)
    print(f"[INFO] Model loaded from '{path}'")
    return model


def ensure_dirs():
    """Create output directories if they don't exist."""
    for d in [DATA_DIR, MODELS_DIR, RESULTS_DIR]:
        os.makedirs(d, exist_ok=True)
