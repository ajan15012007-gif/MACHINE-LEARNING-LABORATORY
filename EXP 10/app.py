"""
Email Spam Detection Using Machine Learning and Naive Bayes
Flask Web Application

College Mini-Project Demonstration
"""

import os
import json
import logging
from flask import Flask, render_template, request, jsonify
import joblib

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "spam_detection_model.pkl")
EVAL_PATH = os.path.join(BASE_DIR, "models", "evaluation_results.json")

# Global variables for in-memory model and evaluation data
model = None
evaluation_data = None


def load_artifacts():
    """
    Load the trained machine learning pipeline and evaluation results.
    Called once at application startup.
    """
    global model, evaluation_data

    # Load Model Pipeline
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            logger.info("Machine learning pipeline loaded successfully from: %s", MODEL_PATH)
        except Exception as e:
            logger.error("Failed to load model pipeline: %s", e)
            model = None
    else:
        logger.warning("Model file not found at '%s'. Run 'python train_model.py' first.", MODEL_PATH)
        model = None

    # Load Evaluation Results JSON
    if os.path.exists(EVAL_PATH):
        try:
            with open(EVAL_PATH, "r", encoding="utf-8") as f:
                evaluation_data = json.load(f)
            logger.info("Evaluation results loaded successfully from: %s", EVAL_PATH)
        except Exception as e:
            logger.error("Failed to load evaluation results: %s", e)
            evaluation_data = None
    else:
        logger.warning("Evaluation results file not found at '%s'.", EVAL_PATH)
        evaluation_data = None


# Initial artifact load
load_artifacts()


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Home page handler.
    Displays project overview, dataset info, EDA visualizations, evaluation metrics,
    and handles prediction form submissions.
    """
    prediction_result = None
    input_message = ""
    error_message = None

    # Handle prediction form POST
    if request.method == "POST":
        input_message = request.form.get("message", "").strip()

        # Input validation
        if not input_message:
            error_message = "Please enter an email or text message to classify. The input cannot be empty."
        elif model is None:
            error_message = "Model pipeline is not loaded. Please ensure 'train_model.py' has been executed."
        else:
            try:
                # Prediction using trained pipeline
                pred_raw = model.predict([input_message])[0]
                proba_arr = model.predict_proba([input_message])[0]

                # Map classes dynamically
                classes = list(model.classes_)
                spam_idx = classes.index("spam")
                ham_idx = classes.index("ham")

                spam_prob = round(float(proba_arr[spam_idx]) * 100, 2)
                ham_prob = round(float(proba_arr[ham_idx]) * 100, 2)

                is_spam = (pred_raw.lower() == "spam")

                prediction_result = {
                    "raw": pred_raw,
                    "is_spam": is_spam,
                    "label": "Spam" if is_spam else "Not Spam (Ham)",
                    "spam_probability": spam_prob,
                    "ham_probability": ham_prob
                }
            except Exception as e:
                logger.error("Error during prediction: %s", e)
                error_message = f"An error occurred during prediction: {str(e)}"

    return render_template(
        "index.html",
        prediction_result=prediction_result,
        input_message=input_message,
        error_message=error_message,
        eval_data=evaluation_data,
        model_ready=(model is not None)
    )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    JSON API endpoint for programmatic message classification.
    """
    if model is None:
        return jsonify({
            "status": "error",
            "message": "Model not loaded. Please run train_model.py first."
        }), 503

    data = request.get_json(silent=True) or request.form
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({
            "status": "error",
            "message": "Message text cannot be empty."
        }), 400

    try:
        pred_raw = model.predict([message])[0]
        proba_arr = model.predict_proba([message])[0]
        classes = list(model.classes_)

        spam_idx = classes.index("spam")
        ham_idx = classes.index("ham")

        is_spam = (pred_raw.lower() == "spam")

        return jsonify({
            "status": "success",
            "message": message,
            "prediction": "Spam" if is_spam else "Not Spam (Ham)",
            "is_spam": is_spam,
            "probabilities": {
                "spam": round(float(proba_arr[spam_idx]) * 100, 2),
                "ham": round(float(proba_arr[ham_idx]) * 100, 2)
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    # Flask local server execution
    print("=================================================================")
    print(" Starting Email Spam Detection Web Application...")
    print(" Open your browser and navigate to: http://127.0.0.1:5000")
    print(" Press Ctrl+C in the terminal to stop the server.")
    print("=================================================================")
    app.run(host="127.0.0.1", port=5000, debug=False)
