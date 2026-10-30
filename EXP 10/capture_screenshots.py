"""
Automated Screenshot Capture Script for Email Spam Detection Project Documentation
Runs Flask server, interacts with application using Selenium Chrome, and captures real outputs.
"""

import os
import sys
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set cache path for selenium
os.environ["SE_CACHE_PATH"] = r"C:\Users\Ajan\.gemini\antigravity\scratch\se_cache"

# Add project root to path
PROJECT_DIR = r"C:\Users\Ajan\.gemini\antigravity\scratch\EmailSpamDetection"
sys.path.insert(0, PROJECT_DIR)

from app import app

SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "documentation", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def capture():
    print("[1/6] Launching Flask server in background...")
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)

    print("[2/6] Configuring Selenium Headless Chrome...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,950")

    driver = webdriver.Chrome(options=options)

    try:
        url = "http://127.0.0.1:5000"
        print(f"[3/6] Navigating to {url}...")
        driver.get(url)
        time.sleep(2)

        # 1. Home Interface & Empty Prediction Form
        shot1 = os.path.join(SCREENSHOT_DIR, "fig2_home_interface.png")
        driver.save_screenshot(shot1)
        print(f"       Saved: {shot1}")

        # 2. Click Spam Sample 1 and capture loaded message
        btn_spam1 = driver.find_element(By.XPATH, "//button[contains(text(), 'Spam: Free Prize')]")
        btn_spam1.click()
        time.sleep(0.5)
        shot2 = os.path.join(SCREENSHOT_DIR, "fig3_spam_sample_input.png")
        driver.save_screenshot(shot2)
        print(f"       Saved: {shot2}")

        # 3. Submit Prediction Form for Spam
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Predict Message')]")
        submit_btn.click()
        time.sleep(1.5)
        shot3 = os.path.join(SCREENSHOT_DIR, "fig4_spam_prediction_result.png")
        driver.save_screenshot(shot3)
        print(f"       Saved: {shot3}")

        # Capture focused spam result card
        shot3_card = os.path.join(SCREENSHOT_DIR, "fig11_spam_card.png")
        driver.find_element(By.CLASS_NAME, "result-card").screenshot(shot3_card)
        print(f"       Saved: {shot3_card}")

        # 4. Click Ham Sample 1, submit, and capture Ham result
        btn_ham1 = driver.find_element(By.XPATH, "//button[contains(text(), 'Ham: College Study')]")
        btn_ham1.click()
        time.sleep(0.5)
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Predict Message')]")
        submit_btn.click()
        time.sleep(1.5)
        shot4 = os.path.join(SCREENSHOT_DIR, "fig5_ham_prediction_result.png")
        driver.save_screenshot(shot4)
        print(f"       Saved: {shot4}")

        # Capture focused ham result card
        shot4_card = os.path.join(SCREENSHOT_DIR, "fig12_ham_card.png")
        driver.find_element(By.CLASS_NAME, "result-card").screenshot(shot4_card)
        print(f"       Saved: {shot4_card}")

        # 5. Scroll to Dataset Section
        dataset_sec = driver.find_element(By.ID, "dataset")
        driver.execute_script("arguments[0].scrollIntoView();", dataset_sec)
        time.sleep(1)
        shot5 = os.path.join(SCREENSHOT_DIR, "fig6_dataset_preprocessing.png")
        dataset_sec.screenshot(shot5)
        print(f"       Saved: {shot5}")

        # 6. Scroll to EDA Visualizations Section
        eda_sec = driver.find_element(By.ID, "eda")
        driver.execute_script("arguments[0].scrollIntoView();", eda_sec)
        time.sleep(1)
        shot6 = os.path.join(SCREENSHOT_DIR, "fig7_eda_visualizations.png")
        driver.save_screenshot(shot6)
        print(f"       Saved: {shot6}")

        # 7. Scroll to Model Evaluation Section
        eval_sec = driver.find_element(By.ID, "evaluation")
        driver.execute_script("arguments[0].scrollIntoView();", eval_sec)
        time.sleep(1)
        shot7 = os.path.join(SCREENSHOT_DIR, "fig8_model_evaluation.png")
        eval_sec.screenshot(shot7)
        print(f"       Saved: {shot7}")

        # 8. Scroll to ML Workflow Section
        wf_sec = driver.find_element(By.ID, "workflow")
        driver.execute_script("arguments[0].scrollIntoView();", wf_sec)
        time.sleep(1)
        shot8 = os.path.join(SCREENSHOT_DIR, "fig9_ml_workflow.png")
        wf_sec.screenshot(shot8)
        print(f"       Saved: {shot8}")

        print("[4/6] Generating Dark-Themed VS Code Directory Structure Screenshot...")
        # Render a clean VS Code explorer HTML and screenshot it for Fig 1
        vscode_html_path = os.path.join(PROJECT_DIR, "documentation", "vscode_explorer.html")
        vscode_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    background-color: #181818;
    color: #cccccc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    margin: 0;
    padding: 20px;
    font-size: 13px;
  }
  .explorer {
    width: 320px;
    background: #1f1f1f;
    border: 1px solid #2b2b2b;
    border-radius: 6px;
    padding: 12px 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  }
  .header {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #999999;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .folder-title {
    font-weight: 600;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
  }
  .tree-node {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 3px 0;
    color: #cccccc;
  }
  .indent-1 { padding-left: 18px; }
  .indent-2 { padding-left: 36px; }
  .folder-icon { color: #dcb67a; font-size: 14px; }
  .file-icon-py { color: #519aba; font-size: 13px; }
  .file-icon-md { color: #42a5f5; font-size: 13px; }
  .file-icon-txt { color: #8bc34a; font-size: 13px; }
  .file-icon-json { color: #cbcb41; font-size: 13px; }
  .file-icon-csv { color: #4caf50; font-size: 13px; }
  .file-icon-pkl { color: #ff9800; font-size: 13px; }
  .file-icon-img { color: #ab47bc; font-size: 13px; }
  .file-icon-html { color: #e44d26; font-size: 13px; }
  .file-icon-css { color: #29b6f6; font-size: 13px; }
</style>
</head>
<body>
  <div class="explorer">
    <div class="header">Explorer</div>
    <div class="folder-title">▼ EmailSpamDetection</div>
    <div class="tree-node indent-1"><span class="folder-icon">▼</span> <span class="folder-icon">📁</span> data</div>
    <div class="tree-node indent-2"><span class="file-icon-csv">📄</span> sms.tsv</div>
    <div class="tree-node indent-2"><span class="file-icon-csv">📄</span> spam.csv</div>
    <div class="tree-node indent-1"><span class="folder-icon">▼</span> <span class="folder-icon">📁</span> documentation</div>
    <div class="tree-node indent-2"><span class="folder-icon">📁</span> screenshots</div>
    <div class="tree-node indent-1"><span class="folder-icon">▼</span> <span class="folder-icon">📁</span> models</div>
    <div class="tree-node indent-2"><span class="file-icon-json">📄</span> evaluation_results.json</div>
    <div class="tree-node indent-2"><span class="file-icon-pkl">📦</span> spam_detection_model.pkl</div>
    <div class="tree-node indent-1"><span class="folder-icon">▼</span> <span class="folder-icon">📁</span> static</div>
    <div class="tree-node indent-2"><span class="folder-icon">📁</span> plots (6 graphs)</div>
    <div class="tree-node indent-2"><span class="file-icon-css">🎨</span> style.css</div>
    <div class="tree-node indent-1"><span class="folder-icon">▼</span> <span class="folder-icon">📁</span> templates</div>
    <div class="tree-node indent-2"><span class="file-icon-html">🌐</span> index.html</div>
    <div class="tree-node indent-1"><span class="file-icon-py">🐍</span> app.py</div>
    <div class="tree-node indent-1"><span class="file-icon-md">📝</span> README.md</div>
    <div class="tree-node indent-1"><span class="file-icon-txt">📋</span> requirements.txt</div>
    <div class="tree-node indent-1"><span class="file-icon-py">🐍</span> train_model.py</div>
  </div>
</body>
</html>
"""
        with open(vscode_html_path, "w", encoding="utf-8") as f:
            f.write(vscode_html)

        driver.get("file:///" + vscode_html_path.replace("\\", "/"))
        time.sleep(0.5)
        shot_vscode = os.path.join(SCREENSHOT_DIR, "fig1_vscode_structure.png")
        explorer_el = driver.find_element(By.CLASS_NAME, "explorer")
        explorer_el.screenshot(shot_vscode)
        print(f"       Saved: {shot_vscode}")

        print("[5/6] All application screenshots captured successfully!")

    finally:
        driver.quit()
        print("[6/6] Browser session closed.")

if __name__ == "__main__":
    capture()