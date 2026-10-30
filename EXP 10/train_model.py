"""
Email Spam Detection Using Machine Learning and Naive Bayes
Training and Evaluation Pipeline Script

Suitable for B.Tech IT College Mini-Project Demonstration
"""

import os
import sys
import json
import tempfile
import urllib.request
import numpy as np
import pandas as pd

# Set matplotlib cache to avoid permission warnings on Windows sandbox
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())
import matplotlib
matplotlib.use("Agg")  # Non-GUI backend for server/script plotting
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import joblib

# Paths configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
PLOTS_DIR = os.path.join(BASE_DIR, "static", "plots")

CSV_PATH = os.path.join(DATA_DIR, "spam.csv")
TSV_PATH = os.path.join(DATA_DIR, "sms.tsv")
MODEL_PATH = os.path.join(MODELS_DIR, "spam_detection_model.pkl")
EVAL_PATH = os.path.join(MODELS_DIR, "evaluation_results.json")

# Ensure required directories exist
for folder in [DATA_DIR, MODELS_DIR, PLOTS_DIR]:
    os.makedirs(folder, exist_ok=True)


def acquire_dataset():
    """
    Ensure the SMS Spam Collection dataset is available locally.
    Checks data/spam.csv, then data/sms.tsv, then attempts online download if missing.
    """
    if os.path.exists(CSV_PATH):
        print(f"[1/10] Found existing dataset at: {CSV_PATH}")
        return

    if os.path.exists(TSV_PATH):
        print(f"[1/10] Found raw TSV dataset at: {TSV_PATH}. Converting to standardized CSV...")
        df_raw = pd.read_csv(TSV_PATH, sep="\t", header=None, names=["label", "message"], encoding="utf-8")
        df_raw.to_csv(CSV_PATH, index=False)
        print(f"       Saved converted dataset to: {CSV_PATH}")
        return

    # If neither exists, attempt automatic download from official UCI mirror
    download_urls = [
        "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv",
        "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
    ]
    print("[1/10] Dataset not found locally. Attempting automatic download...")
    for url in download_urls:
        try:
            print(f"       Trying URL: {url}")
            if url.endswith(".tsv"):
                urllib.request.urlretrieve(url, TSV_PATH)
                df_raw = pd.read_csv(TSV_PATH, sep="\t", header=None, names=["label", "message"], encoding="utf-8")
                df_raw.to_csv(CSV_PATH, index=False)
                print(f"       Successfully downloaded and saved to: {CSV_PATH}")
                return
        except Exception as e:
            print(f"       Download failed from {url}: {e}")

    # If all download attempts fail and file is missing
    print("\n" + "=" * 70)
    print("ERROR: SMS Spam Collection Dataset Not Found!")
    print("=" * 70)
    print("Please place the dataset into the project:")
    print(f"  Target path: {CSV_PATH}")
    print("Download sources:")
    print("  1. UCI Machine Learning Repository:")
    print("     https://archive.ics.uci.edu/dataset/228/sms+spam+collection")
    print("  2. Direct Raw Dataset Mirror:")
    print("     https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv")
    print("Ensure the file has two columns: 'label' (ham/spam) and 'message'.")
    print("=" * 70 + "\n")
    sys.exit(1)


def load_and_preprocess_data():
    """
    Load, validate, clean, and preprocess the dataset.
    Returns cleaned DataFrame and preprocessing metadata summary.
    """
    print("\n[2/10] Loading and inspecting raw dataset...")
    # Support various encodings common in spam datasets
    for enc in ["utf-8", "latin-1", "iso-8859-1", "cp1252"]:
        try:
            df = pd.read_csv(CSV_PATH, encoding=enc)
            break
        except UnicodeDecodeError:
            continue

    initial_shape = df.shape
    print(f"       Raw dataset dimensions: {initial_shape[0]} rows, {initial_shape[1]} columns")
    print(f"       Raw columns detected: {list(df.columns)}")

    # Column name normalization
    # Some Kaggle exports use v1/v2, some use Category/Message, others use label/message
    col_map = {}
    for col in df.columns:
        c_lower = str(col).strip().lower()
        if c_lower in ["v1", "category", "target", "class", "type", "label"]:
            col_map[col] = "label"
        elif c_lower in ["v2", "text", "sms", "email", "content", "message"]:
            col_map[col] = "message"

    if "label" in col_map.values() and "message" in col_map.values():
        df = df.rename(columns=col_map)
        # Keep only the standardized columns
        df = df[["label", "message"]]
    elif "label" not in df.columns or "message" not in df.columns:
        # Check if 1st and 2nd column can be mapped
        df = df.iloc[:, [0, 1]]
        df.columns = ["label", "message"]

    # Missing value handling
    missing_before = df.isnull().sum().to_dict()
    df = df.dropna(subset=["label", "message"]).copy()
    missing_removed = initial_shape[0] - df.shape[0]

    # Label standardization
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    # Normalize labels: e.g. 1 -> spam, 0 -> ham if numeric
    label_replacements = {"1": "spam", "0": "ham", "spam": "spam", "ham": "ham"}
    df["label"] = df["label"].map(lambda x: label_replacements.get(x, x))
    df = df[df["label"].isin(["spam", "ham"])].copy()

    # Message cleaning (strip whitespace, ensure string type, preserve textual words)
    df["message"] = df["message"].astype(str).str.strip()
    df = df[df["message"].str.len() > 0].copy()

    # Calculate message character and word lengths for EDA
    df["char_length"] = df["message"].apply(len)
    df["word_count"] = df["message"].apply(lambda s: len(s.split()))

    # Check and report duplicates
    raw_duplicates = df.duplicated(subset=["message"]).sum()
    print(f"       Duplicate messages detected: {raw_duplicates}")
    # Remove duplicates to prevent data leakage between train and test sets
    df_cleaned = df.drop_duplicates(subset=["message"]).reset_index(drop=True)
    duplicates_removed = len(df) - len(df_cleaned)

    # Save cleaned standardized dataset
    df_cleaned[["label", "message"]].to_csv(CSV_PATH, index=False)

    class_counts = df_cleaned["label"].value_counts().to_dict()
    total_samples = len(df_cleaned)
    ham_count = class_counts.get("ham", 0)
    spam_count = class_counts.get("spam", 0)
    ham_pct = (ham_count / total_samples) * 100 if total_samples > 0 else 0
    spam_pct = (spam_count / total_samples) * 100 if total_samples > 0 else 0

    print(f"       Cleaned dataset dimensions: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")
    print(f"       Class distribution: Ham = {ham_count} ({ham_pct:.2f}%), Spam = {spam_count} ({spam_pct:.2f}%)")
    print(f"       Duplicates removed: {duplicates_removed}")
    print(f"       Missing records removed: {missing_removed}")

    metadata = {
        "raw_total_samples": int(initial_shape[0]),
        "total_samples": int(total_samples),
        "ham_count": int(ham_count),
        "spam_count": int(spam_count),
        "ham_percentage": round(ham_pct, 2),
        "spam_percentage": round(spam_pct, 2),
        "duplicates_removed": int(duplicates_removed),
        "missing_removed": int(missing_removed),
        "avg_ham_length": round(float(df_cleaned[df_cleaned["label"] == "ham"]["char_length"].mean()), 1),
        "avg_spam_length": round(float(df_cleaned[df_cleaned["label"] == "spam"]["char_length"].mean()), 1),
        "first_five_samples": df_cleaned[["label", "message"]].head(5).to_dict(orient="records")
    }

    return df_cleaned, metadata


def generate_eda_visualizations(df):
    """
    Generate all 5 Exploratory Data Analysis (EDA) graphs:
    1. Spam vs Ham Distribution
    2. Message Length Distribution
    3. Message Length Comparison for Spam and Ham
    4. Most Frequent Words in Spam Messages
    5. Most Frequent Words in Ham Messages
    All plots use Seaborn/Matplotlib and are saved to static/plots/
    """
    print("\n[3/10] Generating Exploratory Data Analysis (EDA) visualizations...")
    sns.set_theme(style="whitegrid", font="sans-serif")
    palette = {"ham": "#16a34a", "spam": "#dc2626"}

    # 1. Spam vs Ham Distribution
    plt.figure(figsize=(7, 4.5))
    ax = sns.countplot(data=df, x="label", palette=palette, order=["ham", "spam"], hue="label", legend=False)
    plt.title("Class Distribution: Legitimate (Ham) vs Spam Messages", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Message Category", fontsize=10, fontweight="bold")
    plt.ylabel("Message Count", fontsize=10, fontweight="bold")
    total = len(df)
    for p in ax.patches:
        height = p.get_height()
        pct = (height / total) * 100
        ax.annotate(f"{int(height):,}\n({pct:.1f}%)",
                    (p.get_x() + p.get_width() / 2., height / 2),
                    ha="center", va="center", color="white", fontsize=11, fontweight="bold")
    plt.tight_layout()
    dist_path = os.path.join(PLOTS_DIR, "spam_ham_distribution.png")
    plt.savefig(dist_path, dpi=180)
    plt.close()
    print(f"       Saved: {dist_path}")

    # 2. Overall Message Length Distribution
    plt.figure(figsize=(8, 4.5))
    sns.histplot(df["char_length"], bins=50, kde=True, color="#2563eb", edgecolor="white", alpha=0.7)
    plt.title("Overall Message Length Distribution (Characters)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Message Length in Characters", fontsize=10, fontweight="bold")
    plt.ylabel("Frequency", fontsize=10, fontweight="bold")
    plt.xlim(0, 400)
    plt.tight_layout()
    len_path = os.path.join(PLOTS_DIR, "message_length_distribution.png")
    plt.savefig(len_path, dpi=180)
    plt.close()
    print(f"       Saved: {len_path}")

    # 3. Message Length Comparison for Spam and Ham
    plt.figure(figsize=(8, 4.5))
    sns.histplot(data=df, x="char_length", hue="label", palette=palette,
                 bins=40, kde=True, element="step", common_norm=False, alpha=0.45)
    plt.title("Message Length Comparison: Spam vs Ham", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Message Length in Characters", fontsize=10, fontweight="bold")
    plt.ylabel("Density / Frequency", fontsize=10, fontweight="bold")
    plt.xlim(0, 350)
    plt.legend(title="Category", labels=["Spam", "Ham"])
    plt.tight_layout()
    comp_path = os.path.join(PLOTS_DIR, "message_length_comparison.png")
    plt.savefig(comp_path, dpi=180)
    plt.close()
    print(f"       Saved: {comp_path}")

    # 4 & 5. Most Frequent Words in Spam and Ham (Stopwords removed)
    # Using Scikit-learn's CountVectorizer to reliably extract top unigrams without external wordcloud package
    vec = CountVectorizer(stop_words="english", lowercase=True, token_pattern=r"(?u)\b[a-zA-Z]{2,}\b")

    for category, filename, title_color, bar_color in [
        ("spam", "frequent_spam_words.png", "#dc2626", "#ef4444"),
        ("ham", "frequent_ham_words.png", "#16a34a", "#22c55e")
    ]:
        subset_texts = df[df["label"] == category]["message"]
        X_sub = vec.fit_transform(subset_texts)
        word_counts = np.asarray(X_sub.sum(axis=0)).flatten()
        words = np.array(vec.get_feature_names_out())
        top_indices = np.argsort(word_counts)[-15:][::-1]
        top_words = words[top_indices]
        top_freqs = word_counts[top_indices]

        plt.figure(figsize=(8, 5))
        y_pos = np.arange(len(top_words))
        plt.barh(y_pos, top_freqs, color=bar_color, edgecolor="#cbd5e1", alpha=0.85)
        plt.yticks(y_pos, top_words, fontsize=9.5)
        plt.gca().invert_yaxis()  # Top word at the top
        plt.title(f"Top 15 Most Frequent Words in {category.capitalize()} Messages",
                  fontsize=12, fontweight="bold", color=title_color, pad=12)
        plt.xlabel("Occurrences Count", fontsize=10, fontweight="bold")
        for i, v in enumerate(top_freqs):
            plt.text(v + (max(top_freqs) * 0.01), i, f" {v}", va="center", fontsize=9, color="#1e293b")
        plt.tight_layout()
        plot_file = os.path.join(PLOTS_DIR, filename)
        plt.savefig(plot_file, dpi=180)
        plt.close()
        print(f"       Saved: {plot_file}")


def train_and_evaluate_model(df, metadata):
    """
    Split data into 80% train / 20% test (stratified).
    Compare CountVectorizer vs TfidfVectorizer via CV on training set.
    Build final Pipeline (TfidfVectorizer + MultinomialNB).
    Evaluate on held-out test data.
    Save model artifact and evaluation JSON.
    """
    print("\n[4/10] Splitting dataset into 80% Train and 20% Test (stratified)...")
    X = df["message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    train_counts = y_train.value_counts().to_dict()
    test_counts = y_test.value_counts().to_dict()

    print(f"       Training set: {len(X_train)} samples (Ham: {train_counts.get('ham', 0)}, Spam: {train_counts.get('spam', 0)})")
    print(f"       Testing set:  {len(X_test)} samples (Ham: {test_counts.get('ham', 0)}, Spam: {test_counts.get('spam', 0)})")

    print("\n[5/10] Comparing Text Feature Extractors (CountVectorizer vs TfidfVectorizer on training set)...")
    cv_count = Pipeline([
        ("vectorizer", CountVectorizer(stop_words="english", lowercase=True)),
        ("classifier", MultinomialNB(alpha=1.0))
    ])
    cv_tfidf = Pipeline([
        ("vectorizer", TfidfVectorizer(stop_words="english", lowercase=True)),
        ("classifier", MultinomialNB(alpha=1.0))
    ])

    scores_count = cross_val_score(cv_count, X_train, y_train, cv=5, scoring="f1_macro")
    scores_tfidf = cross_val_score(cv_tfidf, X_train, y_train, cv=5, scoring="f1_macro")
    print(f"       CountVectorizer 5-Fold Macro F1: {scores_count.mean():.4f} (+/- {scores_count.std():.4f})")
    print(f"       TfidfVectorizer 5-Fold Macro F1: {scores_tfidf.mean():.4f} (+/- {scores_tfidf.std():.4f})")

    # Select the top-performing vectorizer based on training cross-validation
    use_count_vec = scores_count.mean() >= scores_tfidf.mean()
    selected_vectorizer_name = "CountVectorizer" if use_count_vec else "TfidfVectorizer"
    print(f"       Selected Feature Extractor based on CV: {selected_vectorizer_name}")

    if use_count_vec:
        vectorizer_step = CountVectorizer(stop_words="english", lowercase=True)
        vec_desc = "CountVectorizer (word frequencies, English stop words removed)"
    else:
        vectorizer_step = TfidfVectorizer(stop_words="english", lowercase=True, sublinear_tf=True)
        vec_desc = "TfidfVectorizer (TF-IDF term weighting, English stop words removed)"

    print(f"\n[6/10] Building final Scikit-learn Pipeline ({selected_vectorizer_name} + MultinomialNB)...")
    pipeline = Pipeline([
        ("vectorizer", vectorizer_step),
        ("classifier", MultinomialNB(alpha=1.0))
    ])

    print("\n[7/10] Fitting pipeline strictly on training data...")
    pipeline.fit(X_train, y_train)

    print("\n[8/10] Evaluating model on held-out test data (positive class: 'spam')...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)

    # Calculate metrics with 'spam' as positive class
    accuracy = accuracy_score(y_test, y_pred)
    precision_spam = precision_score(y_test, y_pred, pos_label="spam")
    recall_spam = recall_score(y_test, y_pred, pos_label="spam")
    f1_spam = f1_score(y_test, y_pred, pos_label="spam")

    # Metrics for ham class
    precision_ham = precision_score(y_test, y_pred, pos_label="ham")
    recall_ham = recall_score(y_test, y_pred, pos_label="ham")
    f1_ham = f1_score(y_test, y_pred, pos_label="ham")

    # Confusion Matrix
    # Labels order: ['ham', 'spam']
    # TN: Actual Ham, Pred Ham
    # FP: Actual Ham, Pred Spam
    # FN: Actual Spam, Pred Ham
    # TP: Actual Spam, Pred Spam
    cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
    tn, fp, fn, tp = cm.ravel()

    print("-" * 60)
    print(f"  Model Accuracy:        {accuracy * 100:.2f}%")
    print(f"  Spam Precision:        {precision_spam * 100:.2f}% (How many flagged as spam were actually spam)")
    print(f"  Spam Recall:           {recall_spam * 100:.2f}% (How many actual spam messages were detected)")
    print(f"  Spam F1-Score:         {f1_spam * 100:.2f}% (Harmonic mean of precision & recall)")
    print(f"  Ham Precision:         {precision_ham * 100:.2f}%")
    print(f"  Ham Recall:            {recall_ham * 100:.2f}%")
    print(f"  True Negatives (TN):   {tn} (Correct Ham)")
    print(f"  False Positives (FP):  {fp} (Legitimate flagged as Spam)")
    print(f"  False Negatives (FN):  {fn} (Spam missed as Ham)")
    print(f"  True Positives (TP):   {tp} (Spam caught)")
    print("-" * 60)

    clf_report_dict = classification_report(y_test, y_pred, output_dict=True)
    clf_report_text = classification_report(y_test, y_pred)
    print("Full Classification Report:\n", clf_report_text)

    # 6. Confusion Matrix Heatmap
    print("\n[9/10] Generating Confusion Matrix Visualization...")
    plt.figure(figsize=(6, 5))
    cm_display_labels = ["Legitimate (Ham)", "Spam"]
    cm_annot = np.array([
        [f"TN: {tn}\n({(tn/len(y_test))*100:.1f}%)", f"FP: {fp}\n({(fp/len(y_test))*100:.1f}%)"],
        [f"FN: {fn}\n({(fn/len(y_test))*100:.1f}%)", f"TP: {tp}\n({(tp/len(y_test))*100:.1f}%)"]
    ])
    sns.heatmap(cm, annot=cm_annot, fmt="", cmap="Blues", cbar=False,
                xticklabels=cm_display_labels, yticklabels=cm_display_labels,
                linewidths=1.5, linecolor="#e2e8f0", annot_kws={"size": 11, "weight": "bold"})
    plt.title("Confusion Matrix on Held-Out Test Set (20%)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Predicted Label", fontsize=10, fontweight="bold")
    plt.ylabel("Actual Label", fontsize=10, fontweight="bold")
    plt.tight_layout()
    cm_path = os.path.join(PLOTS_DIR, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=180)
    plt.close()
    print(f"       Saved: {cm_path}")

    # Save model pipeline
    print("\n[10/10] Saving model pipeline and evaluation report...")
    joblib.dump(pipeline, MODEL_PATH)
    print(f"       Saved trained pipeline: {MODEL_PATH}")

    # Consolidate evaluation results
    eval_data = {
        "dataset_summary": metadata,
        "split_summary": {
            "train_size": len(X_train),
            "test_size": len(X_test),
            "train_ham": int(train_counts.get("ham", 0)),
            "train_spam": int(train_counts.get("spam", 0)),
            "test_ham": int(test_counts.get("ham", 0)),
            "test_spam": int(test_counts.get("spam", 0))
        },
        "model_architecture": {
            "algorithm": "Multinomial Naive Bayes",
            "vectorizer": vec_desc,
            "alpha": 1.0,
            "pipeline_steps": [selected_vectorizer_name, "MultinomialNB"]
        },
        "cv_comparison": {
            "count_vectorizer_f1": round(float(scores_count.mean()), 4),
            "tfidf_vectorizer_f1": round(float(scores_tfidf.mean()), 4)
        },
        "metrics": {
            "accuracy": round(float(accuracy), 4),
            "precision_spam": round(float(precision_spam), 4),
            "recall_spam": round(float(recall_spam), 4),
            "f1_spam": round(float(f1_spam), 4),
            "precision_ham": round(float(precision_ham), 4),
            "recall_ham": round(float(recall_ham), 4),
            "f1_ham": round(float(f1_ham), 4)
        },
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
            "matrix": cm.tolist()
        },
        "classification_report": clf_report_dict
    }

    with open(EVAL_PATH, "w", encoding="utf-8") as f:
        json.dump(eval_data, f, indent=2)
    print(f"       Saved evaluation report: {EVAL_PATH}")

    print("\n" + "=" * 65)
    print(" TRAINING & EVALUATION PIPELINE COMPLETE SUCCESSFULLY!")
    print("=" * 65)
    print(f"  Test Accuracy:    {accuracy * 100:.2f}%")
    print(f"  Spam Precision:   {precision_spam * 100:.2f}%")
    print(f"  Spam Recall:      {recall_spam * 100:.2f}%")
    print(f"  Spam F1-Score:    {f1_spam * 100:.2f}%")
    print("=" * 65 + "\n")


def main():
    print("=================================================================")
    print(" Email Spam Detection Using Machine Learning & Naive Bayes")
    print(" Complete College Mini-Project Training Workflow")
    print("=================================================================")
    acquire_dataset()
    df, metadata = load_and_preprocess_data()
    generate_eda_visualizations(df)
    train_and_evaluate_model(df, metadata)


if __name__ == "__main__":
    main()
