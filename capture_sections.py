"""
Capture each section of training_report.html as a separate PNG image.
Uses Playwright for high-quality element-level screenshots.
"""
import os
import sys
import subprocess


def install_playwright():
    """Install playwright and chromium browser if not available."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[INFO] Installing playwright (first time only)...")
    install_playwright()
    from playwright.sync_api import sync_playwright


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(PROJECT_ROOT, "training_report.html")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "report_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Each section to capture: CSS selector → filename
SECTIONS = [
    {"selector": "#sec-header",    "filename": "01_header.png",          "label": "Header"},
    {"selector": "#sec-code",      "filename": "02_training_code.png",   "label": "Training Code"},
    {"selector": "#sec-terminal",  "filename": "03_terminal_output.png", "label": "Terminal Output"},
    {"selector": "#sec-results",   "filename": "04_results_summary.png", "label": "Results Summary"},
    {"selector": "#sec-reproduce", "filename": "05_how_to_reproduce.png","label": "How to Reproduce"},
]


def main():
    html_url = "file:///" + HTML_FILE.replace("\\", "/")
    print(f"[INFO] Opening: {html_url}")
    print(f"[INFO] Saving PNGs to: {OUTPUT_DIR}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Wide viewport so code doesn't wrap
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(html_url, wait_until="networkidle")
        page.wait_for_timeout(2000)  # wait for fonts

        for section in SECTIONS:
            selector = section["selector"]
            filename = section["filename"]
            label = section["label"]

            try:
                element = page.query_selector(selector)
                if element:
                    path = os.path.join(OUTPUT_DIR, filename)
                    element.screenshot(path=path)
                    size_kb = os.path.getsize(path) / 1024
                    print(f"  OK  {label:25s} -> {filename} ({size_kb:.0f} KB)")
                else:
                    print(f"  FAIL {label:25s} -> Element not found: {selector}")
            except Exception as e:
                print(f"  FAIL {label:25s} -> Error: {e}")

        browser.close()

    print(f"\n[DONE] All section images saved to:")
    print(f"       {OUTPUT_DIR}")
    print("\nYou can now copy-paste these PNGs into your Word document!")


if __name__ == "__main__":
    main()
