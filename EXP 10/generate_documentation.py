"""
Complete Documentation Generator for Email Spam Detection Project
Generates both:
1. Email_Spam_Detection_Project_Documentation.pdf (via ReportLab)
2. Email_Spam_Detection_Project_Documentation.docx (via python-docx)

Strictly follows the structure, formatting, academic style, and 11-page layout of the sample reference PDF.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_DIR = r"C:\Users\Ajan\.gemini\antigravity\scratch\EmailSpamDetection"
DOCS_DIR = os.path.join(PROJECT_DIR, "documentation")
SCREENSHOTS_DIR = os.path.join(DOCS_DIR, "screenshots")
PLOTS_DIR = os.path.join(PROJECT_DIR, "static", "plots")

PDF_PATH = os.path.join(DOCS_DIR, "Email_Spam_Detection_Project_Documentation.pdf")
DOCX_PATH = os.path.join(DOCS_DIR, "Email_Spam_Detection_Project_Documentation.docx")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw page numbers."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        # Draw clean page number at bottom center
        text = f"Page {self._pageNumber} of {page_count}"
        self.drawCentredString(letter[0] / 2.0, 36, text)
        self.restoreState()


def build_pdf():
    print("[1/2] Building Professional PDF Documentation using ReportLab...")
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,   # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define custom typography styles matching sample PDF
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=17,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=10.5,
        leading=14,
        alignment=1,  # Centered
        textColor=colors.HexColor("#334155"),
        spaceAfter=14
    )

    heading_style = ParagraphStyle(
        "DocHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    subheading_style = ParagraphStyle(
        "DocSubHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        alignment=4,  # Justified
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=15,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        "DocCaption",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11.5,
        alignment=1,  # Centered
        textColor=colors.HexColor("#222222"),
        spaceBefore=4,
        spaceAfter=10
    )

    code_text_style = ParagraphStyle(
        "DocCodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.6,
        leading=9.8,
        textColor=colors.HexColor("#0f172a")
    )

    def create_code_box(code_text):
        # Format code lines inside a single-cell table with border and light grey fill
        formatted_code = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
        p = Paragraph(f"<font face='Courier'>{formatted_code}</font>", code_text_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        return t

    story = []

    # =========================================================================
    # PAGE 1: Title, Problem Statement, Objectives, Software/Hardware (Part 1)
    # =========================================================================
    story.append(Paragraph("Email Spam Detection Using Machine Learning and Naive Bayes", title_style))
    story.append(Paragraph("(Email &amp; SMS Spam Classification using Multinomial Naive Bayes)", subtitle_style))

    story.append(Paragraph("Problem Statement:", heading_style))
    p1 = ("Email and SMS communication remain fundamental pillars of global digital correspondence, academic "
          "collaboration, and business transactions. However, the overwhelming volume of unsolicited bulk messages, "
          "phishing attacks, financial scams, and malicious links—collectively known as spam—poses severe security, "
          "privacy, and productivity risks to end users and organizations alike. Traditional keyword-filtering and "
          "rule-based email security systems are fundamentally brittle, as malicious actors easily circumvent static "
          "lexicons through deliberate character obfuscation, zero-day phrasing, homoglyph substitution, and polymorphic "
          "message layouts. Furthermore, manual classification of incoming correspondence is time-consuming, subjective, "
          "and entirely unscalable to the massive influx of daily digital communications.")
    story.append(Paragraph(p1, body_style))

    p2 = ("There is, therefore, a pressing need for an automated, lightweight, and mathematically grounded classification "
          "system capable of analyzing raw message text and reliably discriminating between legitimate (Ham) and fraudulent "
          "(Spam) correspondence with quantifiable posterior class confidence. This project designs, implements, and evaluates "
          "an end-to-end Machine Learning spam classification system employing Natural Language Processing (NLP), text tokenization, "
          "vocabulary feature extraction via CountVectorizer, and probabilistic classification through a Multinomial Naive Bayes "
          "pipeline. The complete system is deployed as an accessible, local web application using the Flask framework, providing "
          "real-time inference, class probability meters, and comprehensive model evaluation based on standard data science metrics "
          "(Accuracy, Precision, Recall, F1-Score, and the Confusion Matrix).")
    story.append(Paragraph(p2, body_style))

    story.append(Paragraph("Objectives:", heading_style))
    objs = [
        "1. To collect, clean, and standardize a real-world benchmark dataset of legitimate (Ham) and Spam messages (UCI SMS Spam Collection).",
        "2. To perform thorough Exploratory Data Analysis (EDA) investigating class imbalance, message character lengths, and discriminative keywords.",
        "3. To extract text features using Bag-of-Words (CountVectorizer) and validate against TF-IDF term weighting via 5-fold cross-validation.",
        "4. To design, train, and serialize an optimal Multinomial Naive Bayes classifier pipeline with Laplace smoothing (&alpha; = 1.0) to prevent zero-frequency likelihoods.",
        "5. To build a responsive, local Flask web application providing real-time message inference with estimated posterior class probabilities.",
        "6. To evaluate the model on an unseen 20% test partition, reporting Accuracy, Precision, Recall, F1-Score, and the Confusion Matrix heatmap."
    ]
    for obj in objs:
        story.append(Paragraph(obj, bullet_style))

    story.append(Paragraph("Software / Hardware Required:", heading_style))
    sw_hw_p1 = [
        "&bull; <b>Operating System:</b> Windows 10/11 / Linux / macOS",
        "&bull; <b>IDE:</b> Visual Studio Code",
        "&bull; <b>Language:</b> Python 3.10+",
        "&bull; <b>Backend Framework:</b> Flask (REST API &amp; Jinja2 Templates)"
    ]
    for item in sw_hw_p1:
        story.append(Paragraph(item, bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Software/Hardware (Part 2), Project Directory Structure (Fig 1)
    # =========================================================================
    sw_hw_p2 = [
        "&bull; <b>Machine Learning:</b> scikit-learn (MultinomialNB, CountVectorizer, TfidfVectorizer, Pipeline, metrics)",
        "&bull; <b>Data Processing &amp; Mathematics:</b> Pandas, NumPy",
        "&bull; <b>Visualizations:</b> Matplotlib, Seaborn",
        "&bull; <b>Model Serialization:</b> Joblib",
        "&bull; <b>Frontend:</b> HTML5, CSS3, JavaScript (Responsive, email-inspired UI)",
        "&bull; <b>Dataset:</b> UCI Machine Learning Repository SMS Spam Collection (5,158 clean records)",
        "&bull; <b>Version Control:</b> Git",
        "&bull; <b>Hardware Requirements:</b> Intel Core i3 / AMD Ryzen 3 / Apple Silicon, 4 GB RAM, 500 MB free disk space"
    ]
    for item in sw_hw_p2:
        story.append(Paragraph(item, bullet_style))

    story.append(Paragraph("Project Directory Structure:", heading_style))
    p_struct = ("The project (<b>“EmailSpamDetection”</b>) is structured modularly with dedicated directories for "
                "the standardized dataset, serialized machine learning artifacts, static exploratory visual plots, Jinja2 "
                "web templates, and backend inference routing, as shown below.")
    story.append(Paragraph(p_struct, body_style))

    fig1_path = os.path.join(SCREENSHOTS_DIR, "fig1_vscode_structure.png")
    if os.path.exists(fig1_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig1_path, width=2.4*inch, height=3.25*inch))
        story.append(Paragraph("<i>Fig 1: Project directory structure of EmailSpamDetection in Visual Studio Code</i>", caption_style))

    struct_desc = ("Key project components include: <b>train_model.py</b> (end-to-end data acquisition, cleaning, EDA generation, "
                   "cross-validation, and model persistence), <b>app.py</b> (Flask web server and prediction endpoints), "
                   "<b>data/spam.csv</b> (deduplicated, standardized dataset), <b>models/spam_detection_model.pkl</b> "
                   "(fitted Scikit-learn pipeline), <b>models/evaluation_results.json</b> (genuine test metrics), "
                   "<b>static/plots/</b> (6 publication-quality graphs), and <b>templates/index.html</b> (interactive user dashboard).")
    story.append(Paragraph(struct_desc, body_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Procedure (1-10) and Implementation Code Header + Module 1 (Part 1)
    # =========================================================================
    story.append(Paragraph("Procedure:", heading_style))
    proc_steps = [
        "1. Collect the authentic SMS Spam Collection dataset from the UCI Machine Learning Repository and store it in <code>data/</code>.",
        "2. Execute <code>train_model.py</code> to load raw text records, inspect structural dimensions, and clean missing values.",
        "3. Standardize column identifiers to <code>label</code> and <code>message</code>, normalize target classes to <code>ham</code> and <code>spam</code>, and remove duplicate messages.",
        "4. Perform Exploratory Data Analysis (EDA) using Matplotlib and Seaborn to visualize class balance, character distributions, and frequent unigram tokens.",
        "5. Partition the cleaned dataset into an 80% training set (4,126 records) and a 20% held-out test set (1,032 records) using stratified sampling (<code>stratify=y</code>).",
        "6. Execute 5-fold cross-validation on the training set to evaluate CountVectorizer against TfidfVectorizer for text representation.",
        "7. Construct a Scikit-learn Pipeline encapsulating CountVectorizer (with English stop-word filtering) and the Multinomial Naive Bayes classifier.",
        "8. Fit the pipeline strictly on the training partition and evaluate generalization performance on the unseen test set (Accuracy, Precision, Recall, F1-Score, Confusion Matrix).",
        "9. Serialize the trained pipeline to <code>models/spam_detection_model.pkl</code> and export test evaluation metrics to <code>models/evaluation_results.json</code>.",
        "10. Launch the Flask web application (<code>app.py</code>), load the saved model pipeline into memory, and classify user-entered messages in real-time."
    ]
    for step in proc_steps:
        story.append(Paragraph(step, bullet_style))

    story.append(Paragraph("Implementation Code:", heading_style))
    p_code_intro = ("Representative implementation of the key modules used in the project, based on the complete "
                    "pipeline executed in the application.")
    story.append(Paragraph(p_code_intro, body_style))

    story.append(Paragraph("1. Data Preprocessing and Cleaning (train_model.py)", subheading_style))
    code_mod1_p1 = """import pandas as pd
import numpy as np

def load_and_preprocess_data(csv_path="data/spam.csv"):
    # Load dataset with fallback encodings
    for enc in ["utf-8", "latin-1", "iso-8859-1"]:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except UnicodeDecodeError:
            continue

    # Standardize column names to 'label' and 'message'
    col_map = {'v1': 'label', 'v2': 'message', 'Category': 'label', 'Message': 'message'}
    df = df.rename(columns={c: col_map[c] for c in df.columns if c in col_map})[["label", "message"]]
    df = df.dropna(subset=["label", "message"]).copy()"""
    story.append(create_code_box(code_mod1_p1))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: Module 1 (Part 2), Module 2 (EDA), Module 3 (Training Part 1)
    # =========================================================================
    code_mod1_p2 = """    # Standardize target labels: ham or spam
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df = df[df["label"].isin(["spam", "ham"])].copy()

    # Deduplication to prevent data leakage between train and test
    df["message"] = df["message"].astype(str).str.strip()
    df_cleaned = df.drop_duplicates(subset=["message"]).reset_index(drop=True)
    df_cleaned["char_length"] = df_cleaned["message"].apply(len)
    return df_cleaned"""
    story.append(create_code_box(code_mod1_p2))

    story.append(Paragraph("2. Exploratory Data Analysis & Visualization (train_model.py)", subheading_style))
    code_mod2 = """import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer

def generate_eda_visualizations(df, plots_dir="static/plots"):
    sns.set_theme(style="whitegrid")
    palette = {"ham": "#16a34a", "spam": "#dc2626"}

    # 1. Class Distribution Plot
    plt.figure(figsize=(7, 4.5))
    ax = sns.countplot(data=df, x="label", palette=palette, order=["ham", "spam"])
    plt.title("Class Distribution: Legitimate (Ham) vs Spam Messages", fontweight="bold")
    plt.savefig(f"{plots_dir}/spam_ham_distribution.png", dpi=180)
    plt.close()

    # 2. Message Length Comparison Plot
    plt.figure(figsize=(8, 4.5))
    sns.histplot(data=df, x="char_length", hue="label", palette=palette, bins=40, kde=True)
    plt.title("Message Length Comparison: Spam vs Ham", fontweight="bold")
    plt.savefig(f"{plots_dir}/message_length_comparison.png", dpi=180)
    plt.close()"""
    story.append(create_code_box(code_mod2))

    story.append(Paragraph("3. Feature Extraction & Model Pipeline Training (train_model.py)", subheading_style))
    code_mod3_p1 = """from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

def train_and_evaluate_model(df):
    X = df["message"]
    y = df["label"]
    # Stratified 80% Train / 20% Held-Out Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )"""
    story.append(create_code_box(code_mod3_p1))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: Module 3 (Part 2: Training & Metrics), Module 4 (Flask Part 1)
    # =========================================================================
    code_mod3_p2 = """    # 5-Fold Cross Validation comparison on training set
    cv_count = Pipeline([("vec", CountVectorizer(stop_words="english")), ("nb", MultinomialNB())])
    cv_tfidf = Pipeline([("vec", TfidfVectorizer(stop_words="english")), ("nb", MultinomialNB())])
    f1_count = cross_val_score(cv_count, X_train, y_train, cv=5, scoring="f1_macro").mean()
    f1_tfidf = cross_val_score(cv_tfidf, X_train, y_train, cv=5, scoring="f1_macro").mean()

    # Build production pipeline with top-performing CountVectorizer
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer(stop_words="english", lowercase=True)),
        ("classifier", MultinomialNB(alpha=1.0))  # Laplace smoothing
    ])
    pipeline.fit(X_train, y_train)

    # Evaluate on held-out test data
    y_pred = pipeline.predict(X_test)
    joblib.dump(pipeline, "models/spam_detection_model.pkl")
    return pipeline, X_test, y_test, y_pred"""
    story.append(create_code_box(code_mod3_p2))

    story.append(Paragraph("4. Prediction Route and Web Application (app.py)", subheading_style))
    code_mod4_p1 = """from flask import Flask, render_template, request, jsonify
import joblib, json

app = Flask(__name__)
# Load trained pipeline and evaluation metadata once at server launch
model = joblib.load("models/spam_detection_model.pkl")
with open("models/evaluation_results.json", "r") as f:
    evaluation_data = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None
    input_message = ""
    error_message = None

    if request.method == "POST":
        input_message = request.form.get("message", "").strip()
        if not input_message:
            error_message = "Please enter an email or text message to classify."
        else:
            # Predict class and estimated posterior probabilities
            pred_raw = model.predict([input_message])[0]
            proba_arr = model.predict_proba([input_message])[0]
            classes = list(model.classes_)"""
    story.append(create_code_box(code_mod4_p1))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: Module 4 (Part 2), Module 5 (Evaluation Export), Output Header + Fig 2
    # =========================================================================
    code_mod4_p2 = """            spam_idx = classes.index("spam")
            ham_idx = classes.index("ham")
            is_spam = (pred_raw.lower() == "spam")

            prediction_result = {
                "raw": pred_raw,
                "is_spam": is_spam,
                "label": "Spam" if is_spam else "Not Spam (Ham)",
                "spam_probability": round(float(proba_arr[spam_idx]) * 100, 2),
                "ham_probability": round(float(proba_arr[ham_idx]) * 100, 2)
            }

    return render_template("index.html", prediction_result=prediction_result,
                           input_message=input_message, error_message=error_message,
                           eval_data=evaluation_data)"""
    story.append(create_code_box(code_mod4_p2))

    story.append(Paragraph("5. Saving Evaluation Metrics and Artifacts (train_model.py)", subheading_style))
    code_mod5 = """from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json

def export_evaluation(y_test, y_pred, eval_path="models/evaluation_results.json"):
    cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
    tn, fp, fn, tp = cm.ravel()
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision_spam": round(precision_score(y_test, y_pred, pos_label="spam"), 4),
        "recall_spam": round(recall_score(y_test, y_pred, pos_label="spam"), 4),
        "f1_spam": round(f1_score(y_test, y_pred, pos_label="spam"), 4),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
    }
    with open(eval_path, "w") as f:
        json.dump(metrics, f, indent=2)"""
    story.append(create_code_box(code_mod5))

    story.append(Paragraph("Output (Step-by-Step Screenshots):", heading_style))

    fig2_path = os.path.join(SCREENSHOTS_DIR, "fig2_home_interface.png")
    if os.path.exists(fig2_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig2_path, width=5.6*inch, height=2.45*inch))
        story.append(Paragraph("<i>Fig 2: Step 1 — Load Input Message: interface to enter email/SMS text or select a benchmark sample</i>", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: Fig 3 (Input Loaded) and Fig 4 (Dataset Summary Table)
    # =========================================================================
    fig3_path = os.path.join(SCREENSHOTS_DIR, "fig3_spam_sample_input.png")
    if os.path.exists(fig3_path):
        story.append(Image(fig3_path, width=5.6*inch, height=2.5*inch))
        story.append(Paragraph("<i>Fig 3: Step 1 — Input message preview after sample spam message is loaded into the form</i>", caption_style))

    fig4_path = os.path.join(SCREENSHOTS_DIR, "fig6_dataset_preprocessing.png")
    if os.path.exists(fig4_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig4_path, width=5.6*inch, height=2.5*inch))
        story.append(Paragraph("<i>Fig 4: Step 2 — Dataset Collection &amp; Preprocessing Summary (5,158 clean samples, 80/20 train-test split)</i>", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: Fig 5 (Class Distribution) and Fig 6 (Length Distribution / Comparison)
    # =========================================================================
    fig5_path = os.path.join(PLOTS_DIR, "spam_ham_distribution.png")
    if os.path.exists(fig5_path):
        story.append(Image(fig5_path, width=4.9*inch, height=2.55*inch))
        story.append(Paragraph("<i>Fig 5: Step 3 — Exploratory Data Analysis: Spam vs Ham Class Distribution (87.55% Ham vs 12.45% Spam)</i>", caption_style))

    fig6_path = os.path.join(PLOTS_DIR, "message_length_comparison.png")
    if os.path.exists(fig6_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig6_path, width=5.1*inch, height=2.55*inch))
        story.append(Paragraph("<i>Fig 6: Step 3 — Exploratory Data Analysis: Message Length Comparison (Spam avg 137.4 chars vs Ham avg 70.9 chars)</i>", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: Fig 7 (Frequent Spam Words) and Fig 8 (Frequent Ham Words)
    # =========================================================================
    fig7_path = os.path.join(PLOTS_DIR, "frequent_spam_words.png")
    if os.path.exists(fig7_path):
        story.append(Image(fig7_path, width=5.1*inch, height=2.55*inch))
        story.append(Paragraph("<i>Fig 7: Step 3 — Exploratory Data Analysis: Top 15 Frequent Words in Spam Messages (commercial &amp; urgent unigrams)</i>", caption_style))

    fig8_path = os.path.join(PLOTS_DIR, "frequent_ham_words.png")
    if os.path.exists(fig8_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig8_path, width=5.1*inch, height=2.55*inch))
        story.append(Paragraph("<i>Fig 8: Step 3 — Exploratory Data Analysis: Top 15 Frequent Words in Legitimate (Ham) Messages (conversational unigrams)</i>", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: Fig 9 (Confusion Matrix Heatmap) and Fig 10 (Spam Result Card)
    # =========================================================================
    fig9_path = os.path.join(PLOTS_DIR, "confusion_matrix.png")
    if os.path.exists(fig9_path):
        story.append(Image(fig9_path, width=4.5*inch, height=2.7*inch))
        story.append(Paragraph("<i>Fig 9: Step 4 — Confusion Matrix Heatmap on Unseen Held-Out Test Set (TN=899, FP=5, FN=12, TP=116)</i>", caption_style))

    fig10_path = os.path.join(SCREENSHOTS_DIR, "fig11_spam_card.png")
    if os.path.exists(fig10_path):
        story.append(Spacer(1, 4))
        story.append(Image(fig10_path, width=5.0*inch, height=2.4*inch))
        story.append(Paragraph("<i>Fig 10: Step 5 — Classification result: Spam Message Detected (100.0% Spam Confidence, 0.0% Ham)</i>", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: Fig 11 (Ham Result Card), Fig 12 (Evaluation Metrics), and Result
    # =========================================================================
    fig11_path = os.path.join(SCREENSHOTS_DIR, "fig12_ham_card.png")
    if os.path.exists(fig11_path):
        story.append(Image(fig11_path, width=5.0*inch, height=2.25*inch))
        story.append(Paragraph("<i>Fig 11: Step 5 — Classification result: Legitimate Message (Ham) Detected (99.9% Ham Confidence, 0.1% Spam)</i>", caption_style))

    fig12_path = os.path.join(SCREENSHOTS_DIR, "fig8_model_evaluation.png")
    if os.path.exists(fig12_path):
        story.append(Spacer(1, 3))
        story.append(Image(fig12_path, width=5.5*inch, height=2.25*inch))
        story.append(Paragraph("<i>Fig 12: Step 6 — Performance evaluation metrics (Accuracy 98.35%, Precision 95.87%, Recall 90.62%, F1-Score 93.17%)</i>", caption_style))

    story.append(Paragraph("Result:", heading_style))
    p_result = ("A web-based Email and SMS Spam Detection system was successfully designed, trained, evaluated, "
                "and deployed using a Flask backend, Scikit-learn machine learning pipeline, and the real UCI SMS Spam "
                "Collection benchmark dataset. Raw messages were preprocessed to remove 414 duplicate records, standardizing "
                "5,158 clean samples. Unigram word counts were extracted using CountVectorizer, and a Multinomial Naive "
                "Bayes classifier with Laplace smoothing (&alpha; = 1.0) was trained on an 80% stratified training partition. "
                "On the held-out 20% test dataset (1,032 unseen messages), the model achieved an outstanding <b>Accuracy of 98.35%</b>, "
                "<b>Spam Precision of 95.87%</b>, <b>Spam Recall of 90.62%</b>, and a <b>Macro F1-Score of 93.17%</b>, with only "
                "5 False Positives out of 904 legitimate emails. The trained pipeline is serialized to disk and integrated into "
                "an interactive, responsive Flask web application that provides real-time classification and estimated posterior "
                "class probabilities.")
    story.append(Paragraph(p_result, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"       Successfully generated PDF: {PDF_PATH}")


def build_docx():
    print("[2/2] Building Editable DOCX Documentation using python-docx...")
    doc = docx.Document()

    # Set 0.75 in margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    def set_font(run, name="Helvetica", size=10, bold=False, italic=False, color=(30, 41, 59)):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        set_font(run, name="Arial", size=13.5, bold=True, color=(15, 23, 42))

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        set_font(run, name="Arial", size=10.5, italic=True, color=(51, 65, 85))

    def add_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        set_font(run, name="Arial", size=11, bold=True, color=(15, 23, 42))

    def add_subheading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        set_font(run, name="Arial", size=10, bold=True, color=(30, 41, 59))

    def add_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        set_font(run, name="Arial", size=9.5, color=(30, 41, 59))

    def add_bullet(text):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        set_font(run, name="Arial", size=9.5, color=(30, 41, 59))

    def add_code_box(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.8)

        # Light gray background and thin border
        shading = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)

        borders = parse_xml(
            r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            r'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            r'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            r'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/></w:tcBorders>'.format(nsdecls('w'))
        )
        cell._tc.get_or_add_tcPr().append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(code_text)
        set_font(run, name="Courier New", size=7.8, color=(15, 23, 42))

        doc.add_paragraph().paragraph_format.space_after = Pt(3)

    def add_fig(img_path, caption, width_in=5.4):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            p.add_run().add_picture(img_path, width=Inches(width_in))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            run = p_cap.add_run(caption)
            set_font(run, name="Arial", size=8.5, italic=True, color=(34, 34, 34))

    # --- Page 1 ---
    add_title("Email Spam Detection Using Machine Learning and Naive Bayes")
    add_subtitle("(Email & SMS Spam Classification using Multinomial Naive Bayes)")

    add_heading("Problem Statement:")
    add_body("Email and SMS communication remain fundamental pillars of global digital correspondence, academic "
             "collaboration, and business transactions. However, the overwhelming volume of unsolicited bulk messages, "
             "phishing attacks, financial scams, and malicious links—collectively known as spam—poses severe security, "
             "privacy, and productivity risks to end users and organizations alike. Traditional keyword-filtering and "
             "rule-based email security systems are fundamentally brittle, as malicious actors easily circumvent static "
             "lexicons through deliberate character obfuscation, zero-day phrasing, homoglyph substitution, and polymorphic "
             "message layouts. Furthermore, manual classification of incoming correspondence is time-consuming, subjective, "
             "and entirely unscalable to the massive influx of daily digital communications.")

    add_body("There is, therefore, a pressing need for an automated, lightweight, and mathematically grounded classification "
             "system capable of analyzing raw message text and reliably discriminating between legitimate (Ham) and fraudulent "
             "(Spam) correspondence with quantifiable posterior class confidence. This project designs, implements, and evaluates "
             "an end-to-end Machine Learning spam classification system employing Natural Language Processing (NLP), text tokenization, "
             "vocabulary feature extraction via CountVectorizer, and probabilistic classification through a Multinomial Naive Bayes "
             "pipeline. The complete system is deployed as an accessible, local web application using the Flask framework, providing "
             "real-time inference, class probability meters, and comprehensive model evaluation based on standard data science metrics "
             "(Accuracy, Precision, Recall, F1-Score, and the Confusion Matrix).")

    add_heading("Objectives:")
    add_bullet("1. To collect, clean, and standardize a real-world benchmark dataset of legitimate (Ham) and Spam messages (UCI SMS Spam Collection).")
    add_bullet("2. To perform thorough Exploratory Data Analysis (EDA) investigating class imbalance, message character lengths, and discriminative keywords.")
    add_bullet("3. To extract text features using Bag-of-Words (CountVectorizer) and validate against TF-IDF term weighting via 5-fold cross-validation.")
    add_bullet("4. To design, train, and serialize an optimal Multinomial Naive Bayes classifier pipeline with Laplace smoothing (α = 1.0) to prevent zero-frequency likelihoods.")
    add_bullet("5. To build a responsive, local Flask web application providing real-time message inference with estimated posterior class probabilities.")
    add_bullet("6. To evaluate the model on an unseen 20% test partition, reporting Accuracy, Precision, Recall, F1-Score, and the Confusion Matrix heatmap.")

    add_heading("Software / Hardware Required:")
    add_bullet("Operating System: Windows 10/11 / Linux / macOS")
    add_bullet("IDE: Visual Studio Code")
    add_bullet("Language: Python 3.10+")
    add_bullet("Backend Framework: Flask (REST API & Jinja2 Templates)")

    doc.add_page_break()

    # --- Page 2 ---
    add_bullet("Machine Learning: scikit-learn (MultinomialNB, CountVectorizer, TfidfVectorizer, Pipeline, metrics)")
    add_bullet("Data Processing & Mathematics: Pandas, NumPy")
    add_bullet("Visualizations: Matplotlib, Seaborn")
    add_bullet("Model Serialization: Joblib")
    add_bullet("Frontend: HTML5, CSS3, JavaScript (Responsive, email-inspired UI)")
    add_bullet("Dataset: UCI Machine Learning Repository SMS Spam Collection (5,158 clean records)")
    add_bullet("Version Control: Git")
    add_bullet("Hardware Requirements: Intel Core i3 / AMD Ryzen 3 / Apple Silicon, 4 GB RAM, 500 MB free disk space")

    add_heading("Project Directory Structure:")
    add_body("The project (“EmailSpamDetection”) is structured modularly with dedicated directories for "
             "the standardized dataset, serialized machine learning artifacts, static exploratory visual plots, Jinja2 "
             "web templates, and backend inference routing, as shown below.")

    add_fig(os.path.join(SCREENSHOTS_DIR, "fig1_vscode_structure.png"),
            "Fig 1: Project directory structure of EmailSpamDetection in Visual Studio Code", width_in=2.4)

    add_body("Key project components include: train_model.py (end-to-end data acquisition, cleaning, EDA generation, "
             "cross-validation, and model persistence), app.py (Flask web server and prediction endpoints), "
             "data/spam.csv (deduplicated, standardized dataset), models/spam_detection_model.pkl "
             "(fitted Scikit-learn pipeline), models/evaluation_results.json (genuine test metrics), "
             "static/plots/ (6 publication-quality graphs), and templates/index.html (interactive user dashboard).")

    doc.add_page_break()

    # --- Page 3 ---
    add_heading("Procedure:")
    add_bullet("1. Collect the authentic SMS Spam Collection dataset from the UCI Machine Learning Repository and store it in data/.")
    add_bullet("2. Execute train_model.py to load raw text records, inspect structural dimensions, and clean missing values.")
    add_bullet("3. Standardize column identifiers to label and message, normalize target classes to ham and spam, and remove duplicate messages.")
    add_bullet("4. Perform Exploratory Data Analysis (EDA) using Matplotlib and Seaborn to visualize class balance, character distributions, and frequent unigram tokens.")
    add_bullet("5. Partition the cleaned dataset into an 80% training set (4,126 records) and a 20% held-out test set (1,032 records) using stratified sampling (stratify=y).")
    add_bullet("6. Execute 5-fold cross-validation on the training set to evaluate CountVectorizer against TfidfVectorizer for text representation.")
    add_bullet("7. Construct a Scikit-learn Pipeline encapsulating CountVectorizer (with English stop-word filtering) and the Multinomial Naive Bayes classifier.")
    add_bullet("8. Fit the pipeline strictly on the training partition and evaluate generalization performance on the unseen test set (Accuracy, Precision, Recall, F1-Score, Confusion Matrix).")
    add_bullet("9. Serialize the trained pipeline to models/spam_detection_model.pkl and export test evaluation metrics to models/evaluation_results.json.")
    add_bullet("10. Launch the Flask web application (app.py), load the saved model pipeline into memory, and classify user-entered messages in real-time.")

    add_heading("Implementation Code:")
    add_body("Representative implementation of the key modules used in the project, based on the complete pipeline executed in the application.")

    add_subheading("1. Data Preprocessing and Cleaning (train_model.py)")
    add_code_box(
"""import pandas as pd
import numpy as np

def load_and_preprocess_data(csv_path="data/spam.csv"):
    for enc in ["utf-8", "latin-1", "iso-8859-1"]:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except UnicodeDecodeError:
            continue

    col_map = {'v1': 'label', 'v2': 'message', 'Category': 'label', 'Message': 'message'}
    df = df.rename(columns={c: col_map[c] for c in df.columns if c in col_map})[["label", "message"]]
    df = df.dropna(subset=["label", "message"]).copy()"""
    )

    doc.add_page_break()

    # --- Page 4 ---
    add_code_box(
"""    # Standardize target labels: ham or spam
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df = df[df["label"].isin(["spam", "ham"])].copy()

    # Deduplication to prevent data leakage between train and test
    df["message"] = df["message"].astype(str).str.strip()
    df_cleaned = df.drop_duplicates(subset=["message"]).reset_index(drop=True)
    df_cleaned["char_length"] = df_cleaned["message"].apply(len)
    return df_cleaned"""
    )

    add_subheading("2. Exploratory Data Analysis & Visualization (train_model.py)")
    add_code_box(
"""import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer

def generate_eda_visualizations(df, plots_dir="static/plots"):
    sns.set_theme(style="whitegrid")
    palette = {"ham": "#16a34a", "spam": "#dc2626"}

    # 1. Class Distribution Plot
    plt.figure(figsize=(7, 4.5))
    ax = sns.countplot(data=df, x="label", palette=palette, order=["ham", "spam"])
    plt.title("Class Distribution: Legitimate (Ham) vs Spam Messages", fontweight="bold")
    plt.savefig(f"{plots_dir}/spam_ham_distribution.png", dpi=180)
    plt.close()

    # 2. Message Length Comparison Plot
    plt.figure(figsize=(8, 4.5))
    sns.histplot(data=df, x="char_length", hue="label", palette=palette, bins=40, kde=True)
    plt.title("Message Length Comparison: Spam vs Ham", fontweight="bold")
    plt.savefig(f"{plots_dir}/message_length_comparison.png", dpi=180)
    plt.close()"""
    )

    add_subheading("3. Feature Extraction & Model Pipeline Training (train_model.py)")
    add_code_box(
"""from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

def train_and_evaluate_model(df):
    X = df["message"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )"""
    )

    doc.add_page_break()

    # --- Page 5 ---
    add_code_box(
"""    # 5-Fold Cross Validation comparison on training set
    cv_count = Pipeline([("vec", CountVectorizer(stop_words="english")), ("nb", MultinomialNB())])
    cv_tfidf = Pipeline([("vec", TfidfVectorizer(stop_words="english")), ("nb", MultinomialNB())])
    f1_count = cross_val_score(cv_count, X_train, y_train, cv=5, scoring="f1_macro").mean()
    f1_tfidf = cross_val_score(cv_tfidf, X_train, y_train, cv=5, scoring="f1_macro").mean()

    # Build production pipeline with top-performing CountVectorizer
    pipeline = Pipeline([
        ("vectorizer", CountVectorizer(stop_words="english", lowercase=True)),
        ("classifier", MultinomialNB(alpha=1.0))  # Laplace smoothing
    ])
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    joblib.dump(pipeline, "models/spam_detection_model.pkl")
    return pipeline, X_test, y_test, y_pred"""
    )

    add_subheading("4. Prediction Route and Web Application (app.py)")
    add_code_box(
"""from flask import Flask, render_template, request, jsonify
import joblib, json

app = Flask(__name__)
model = joblib.load("models/spam_detection_model.pkl")
with open("models/evaluation_results.json", "r") as f:
    evaluation_data = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None
    input_message = ""
    error_message = None

    if request.method == "POST":
        input_message = request.form.get("message", "").strip()
        if not input_message:
            error_message = "Please enter an email or text message to classify."
        else:
            pred_raw = model.predict([input_message])[0]
            proba_arr = model.predict_proba([input_message])[0]
            classes = list(model.classes_)"""
    )

    doc.add_page_break()

    # --- Page 6 ---
    add_code_box(
"""            spam_idx = classes.index("spam")
            ham_idx = classes.index("ham")
            is_spam = (pred_raw.lower() == "spam")

            prediction_result = {
                "raw": pred_raw,
                "is_spam": is_spam,
                "label": "Spam" if is_spam else "Not Spam (Ham)",
                "spam_probability": round(float(proba_arr[spam_idx]) * 100, 2),
                "ham_probability": round(float(proba_arr[ham_idx]) * 100, 2)
            }

    return render_template("index.html", prediction_result=prediction_result,
                           input_message=input_message, error_message=error_message,
                           eval_data=evaluation_data)"""
    )

    add_subheading("5. Saving Evaluation Metrics and Artifacts (train_model.py)")
    add_code_box(
"""from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json

def export_evaluation(y_test, y_pred, eval_path="models/evaluation_results.json"):
    cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
    tn, fp, fn, tp = cm.ravel()
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision_spam": round(precision_score(y_test, y_pred, pos_label="spam"), 4),
        "recall_spam": round(recall_score(y_test, y_pred, pos_label="spam"), 4),
        "f1_spam": round(f1_score(y_test, y_pred, pos_label="spam"), 4),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}
    }
    with open(eval_path, "w") as f:
        json.dump(metrics, f, indent=2)"""
    )

    add_heading("Output (Step-by-Step Screenshots):")
    add_fig(os.path.join(SCREENSHOTS_DIR, "fig2_home_interface.png"),
            "Fig 2: Step 1 — Load Input Message: interface to enter email/SMS text or select a benchmark sample", width_in=5.4)

    doc.add_page_break()

    # --- Page 7 ---
    add_fig(os.path.join(SCREENSHOTS_DIR, "fig3_spam_sample_input.png"),
            "Fig 3: Step 1 — Input message preview after sample spam message is loaded into the form", width_in=5.4)
    add_fig(os.path.join(SCREENSHOTS_DIR, "fig6_dataset_preprocessing.png"),
            "Fig 4: Step 2 — Dataset Collection & Preprocessing Summary (5,158 clean samples, 80/20 train-test split)", width_in=5.4)

    doc.add_page_break()

    # --- Page 8 ---
    add_fig(os.path.join(PLOTS_DIR, "spam_ham_distribution.png"),
            "Fig 5: Step 3 — Exploratory Data Analysis: Spam vs Ham Class Distribution (87.55% Ham vs 12.45% Spam)", width_in=4.8)
    add_fig(os.path.join(PLOTS_DIR, "message_length_comparison.png"),
            "Fig 6: Step 3 — Exploratory Data Analysis: Message Length Comparison (Spam avg 137.4 chars vs Ham avg 70.9 chars)", width_in=5.0)

    doc.add_page_break()

    # --- Page 9 ---
    add_fig(os.path.join(PLOTS_DIR, "frequent_spam_words.png"),
            "Fig 7: Step 3 — Exploratory Data Analysis: Top 15 Frequent Words in Spam Messages (commercial & urgent unigrams)", width_in=5.0)
    add_fig(os.path.join(PLOTS_DIR, "frequent_ham_words.png"),
            "Fig 8: Step 3 — Exploratory Data Analysis: Top 15 Frequent Words in Legitimate (Ham) Messages (conversational unigrams)", width_in=5.0)

    doc.add_page_break()

    # --- Page 10 ---
    add_fig(os.path.join(PLOTS_DIR, "confusion_matrix.png"),
            "Fig 9: Step 4 — Confusion Matrix Heatmap on Unseen Held-Out Test Set (TN=899, FP=5, FN=12, TP=116)", width_in=4.4)
    add_fig(os.path.join(SCREENSHOTS_DIR, "fig11_spam_card.png"),
            "Fig 10: Step 5 — Classification result: Spam Message Detected (100.0% Spam Confidence, 0.0% Ham)", width_in=4.8)

    doc.add_page_break()

    # --- Page 11 ---
    add_fig(os.path.join(SCREENSHOTS_DIR, "fig12_ham_card.png"),
            "Fig 11: Step 5 — Classification result: Legitimate Message (Ham) Detected (99.9% Ham Confidence, 0.1% Spam)", width_in=4.8)
    add_fig(os.path.join(SCREENSHOTS_DIR, "fig8_model_evaluation.png"),
            "Fig 12: Step 6 — Performance evaluation metrics (Accuracy 98.35%, Precision 95.87%, Recall 90.62%, F1-Score 93.17%)", width_in=5.4)

    add_heading("Result:")
    add_body("A web-based Email and SMS Spam Detection system was successfully designed, trained, evaluated, "
             "and deployed using a Flask backend, Scikit-learn machine learning pipeline, and the real UCI SMS Spam "
             "Collection benchmark dataset. Raw messages were preprocessed to remove 414 duplicate records, standardizing "
             "5,158 clean samples. Unigram word counts were extracted using CountVectorizer, and a Multinomial Naive "
             "Bayes classifier with Laplace smoothing (α = 1.0) was trained on an 80% stratified training partition. "
             "On the held-out 20% test dataset (1,032 unseen messages), the model achieved an outstanding Accuracy of 98.35%, "
             "Spam Precision of 95.87%, Spam Recall of 90.62%, and a Macro F1-Score of 93.17%, with only "
             "5 False Positives out of 904 legitimate emails. The trained pipeline is serialized to disk and integrated into "
             "an interactive, responsive Flask web application that provides real-time classification and estimated posterior "
             "class probabilities.")

    doc.save(DOCX_PATH)
    print(f"       Successfully generated DOCX: {DOCX_PATH}")


if __name__ == "__main__":
    build_pdf()
    build_docx()
    print("\nDocumentation generation complete!")
