"""
app.py
------
Flask web interface for the Phishing Detection System.

Provides a simple, clean web UI where users can submit URLs
and receive instant classification results.

Run:
    python app/app.py

Then open http://localhost:5000 in your browser.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, send_from_directory
from src.predict import classify_url
from src.utils import load_model

app = Flask(__name__)

# Load model once at startup
_model = None


def get_model():
    """Lazy-load the trained model."""
    global _model
    if _model is None:
        try:
            _model = load_model()
        except FileNotFoundError:
            return None
    return _model


@app.route("/", methods=["GET"])
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/results/<path:filename>", methods=["GET"])
def serve_results(filename):
    """Serve trained model evaluation graphs."""
    results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
    return send_from_directory(results_dir, filename)


@app.route("/predict", methods=["POST"])
def predict():
    """Handle URL classification requests."""
    # Handle AJAX JSON requests or traditional form submits
    is_ajax = (
        request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.args.get("format") == "json"
    )

    if request.is_json:
        data = request.get_json() or {}
        url = data.get("url", "").strip()
    else:
        url = request.form.get("url", "").strip()

    if not url:
        if is_ajax:
            return jsonify({"success": False, "error": "Please enter a URL to analyse."}), 400
        return render_template("index.html", error="Please enter a URL to analyse.")

    # Basic URL validation
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    m = get_model()
    if m is None:
        err_msg = "Model not found. Run 'python src/train_model.py' first."
        if is_ajax:
            return jsonify({"success": False, "error": err_msg}), 500
        return render_template("index.html", error=err_msg)

    # Classify using the predict module
    result = classify_url(url, model=m)

    feature_details = []
    for name, val in result["features"].items():
        status = {1: "Safe", 0: "Suspicious", -1: "Dangerous"}[val]
        feature_details.append({"name": name, "value": val, "status": status})

    if is_ajax:
        return jsonify({
            "success": True,
            "url": url,
            "is_phishing": result["is_phishing"],
            "label": result["label"],
            "prediction": result["prediction"],
            "features": feature_details
        })

    return render_template(
        "index.html",
        url=url,
        is_phishing=result["is_phishing"],
        label=result["label"],
        prediction=result["prediction"],
        features=feature_details,
        show_result=True,
    )


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  PHISHING DETECTION SYSTEM — WEB INTERFACE")
    print("=" * 55)
    print("  Open http://localhost:5000 in your browser")
    print("=" * 55 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
