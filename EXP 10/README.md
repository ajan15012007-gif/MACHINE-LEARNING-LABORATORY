# Email Spam Detection Using Machine Learning and Naive Bayes

A complete, production-grade Machine Learning mini project built using **Python, Scikit-learn, and Flask**, designed specifically for **B.Tech Information Technology (IT) college laboratory and project demonstrations**.

The project accurately classifies incoming emails and SMS messages into **Spam** or **Not Spam (Ham)** using a trained **Multinomial Naive Bayes** pipeline and the benchmark **UCI SMS Spam Collection** dataset.

---

## 1. Project Objective

The primary objective is to build an interactive, locally hosted web application that predicts whether user-entered email or SMS messages are legitimate (**Ham**) or fraudulent (**Spam**).

- **Example Spam Input:**  
  `"Congratulations! You have won a free prize. Claim now!"`  
  **Predicted Category:** `Spam` (Spam Probability: ~99%)

- **Example Ham Input:**  
  `"Hi, are you coming to college tomorrow?"`  
  **Predicted Category:** `Not Spam (Ham)` (Ham Probability: ~99%)

All predictions and class probabilities are generated in real-time by a Scikit-learn machine learning pipeline trained strictly on real-world benchmark data.

---

## 2. Technologies Used

| Category | Technologies |
| :--- | :--- |
| **Programming Language** | Python 3.10+ |
| **Machine Learning** | Scikit-learn (`MultinomialNB`, `CountVectorizer`, `TfidfVectorizer`, `Pipeline`) |
| **Data Processing** | Pandas, NumPy |
| **Visualizations (EDA)** | Matplotlib, Seaborn |
| **Model Persistence** | Joblib |
| **Backend Framework** | Flask (Jinja2 Templates) |
| **Frontend UI** | HTML5, CSS3, JavaScript (Responsive, email-inspired UI) |
| **Target Environment** | Local machine (VS Code on Windows, macOS, or Linux) |

*No paid APIs, cloud services, or external subscriptions required.*

---

## 3. Project Structure

```text
EmailSpamDetection/
├── app.py                              # Flask web application & prediction endpoints
├── train_model.py                      # Data preprocessing, EDA generation, & ML training pipeline
├── requirements.txt                    # Project library dependencies
├── README.md                           # Comprehensive documentation & setup instructions
├── data/
│   ├── spam.csv                        # Standardized, cleaned dataset (5,158 records)
│   └── sms.tsv                         # Raw UCI SMS Spam Collection benchmark file
├── models/
│   ├── spam_detection_model.pkl        # Serialized Scikit-learn pipeline (Joblib)
│   └── evaluation_results.json         # Genuine test metrics and dataset summary (JSON)
├── static/
│   ├── style.css                       # Responsive email-inspired styling
│   └── plots/                          # EDA & model evaluation visualizations
│       ├── spam_ham_distribution.png
│       ├── message_length_distribution.png
│       ├── message_length_comparison.png
│       ├── frequent_spam_words.png
│       ├── frequent_ham_words.png
│       └── confusion_matrix.png
└── templates/
    └── index.html                      # Interactive web dashboard & presentation UI
```

---

## 4. Dataset Source and Acquisition

This project uses the real, widely cited **SMS Spam Collection Dataset** originally contributed to the **UCI Machine Learning Repository** by Tiago A. Almeida and José María Gómez Hidalgo.

- **Total Messages:** 5,572 raw messages (5,158 unique messages after deduplication).
- **Class Breakdown:**
  - **Legitimate (Ham):** 4,516 messages (87.55%)
  - **Spam:** 642 messages (12.45%)
- **Data Columns:**
  - `label`: Target class (`ham` or `spam`)
  - `message`: Text content of the SMS or email message

### Automatic Download
The training script `train_model.py` automatically checks for `data/spam.csv` or `data/sms.tsv`. If neither exists, it fetches the original dataset directly from:
`https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv`

### Manual Placement (Offline Setup)
If running on an offline machine without internet access:
1. Download `sms.tsv` or `spam.csv` from [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/228/sms+spam+collection).
2. Save the file into the `data/` folder as `data/spam.csv`.
3. Verify that the file contains two columns: `label` and `message`.

---

## 5. Machine Learning Workflow

The project follows the complete 10-step data science lifecycle:

```text
1. Problem Definition  ──► Binary classification of text into Ham or Spam
2. Dataset Collection  ──► Real UCI SMS Spam Collection benchmark
3. Data Preprocessing  ──► Missing record handling, deduplication, label normalization
4. Exploratory Data    ──► Distribution plots, length comparisons, frequent unigrams
5. Feature Extraction  ──► Bag-of-Words Vectorization (CountVectorizer / TF-IDF)
6. Train-Test Split    ──► Stratified 80% Train (4,126) / 20% Held-Out Test (1,032)
7. Model Training      ──► Multinomial Naive Bayes (Laplace smoothing α = 1.0)
8. Model Evaluation    ──► Accuracy, Precision, Recall, F1-Score, Confusion Matrix
9. Model Serialization ──► Fitted Pipeline saved to models/spam_detection_model.pkl
10. Web Deployment     ──► Real-time local inference through Flask web dashboard
```

---

## 6. Theory & Concepts Explained

### Text Feature Extraction
Machine learning algorithms operate on numerical vectors, not raw text strings. We use **CountVectorizer** from Scikit-learn:
- Converts each message into a vector of token frequencies.
- Automatically handles tokenization, lowercasing, and strips common English stop words (*the, is, at, which*).
- Prevents data leakage by fitting vector vocabulary strictly on the **80% training set** and transforming the test set and live inputs.

### Multinomial Naive Bayes Algorithm
Based on **Bayes' Theorem** with the "naive" assumption of conditional feature independence:

$$P(\text{Spam} \mid \mathbf{w}) = \frac{P(\text{Spam}) \prod_{i=1}^n P(w_i \mid \text{Spam})}{P(\mathbf{w})}$$

Where:
- $P(\text{Spam})$ is the prior probability of spam.
- $P(w_i \mid \text{Spam})$ is the conditional likelihood of observing word $w_i$ in spam messages.
- **Laplace Smoothing ($\alpha = 1.0$):** Adds a pseudo-count of 1 to all word counts so that words unseen during training never result in a zero probability product.

---

## 7. Model Performance & Evaluation Results

Evaluated strictly on the held-out **20% test dataset** ($n = 1,032$ messages):

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Overall Accuracy** | **98.35%** | Percentage of all test messages correctly classified |
| **Spam Precision** | **95.87%** | Out of all messages flagged as spam, 95.87% were true spam |
| **Spam Recall** | **90.62%** | Out of all actual spam messages, 90.62% were detected |
| **Spam F1-Score** | **93.17%** | Harmonic mean balancing precision and recall |
| **Ham Precision** | **98.68%** | Precision for legitimate messages |
| **Ham Recall** | **99.45%** | Recall for legitimate messages |

### Confusion Matrix (Test Set: 1,032 samples)
- **True Negatives (TN):** 899 legitimate messages correctly labeled as Ham
- **False Positives (FP):** 5 legitimate messages incorrectly flagged as Spam
- **False Negatives (FN):** 12 spam messages missed as Ham
- **True Positives (TP):** 116 spam messages correctly caught

### Critical Note on False Positives vs False Negatives
In email spam filtering, **False Positives** are far more critical than False Negatives:
- An **FP** causes an important email (e.g. university admission, job offer, or password reset) to be lost in the spam folder.
- An **FN** is merely a mild nuisance where a junk message arrives in the inbox.
- Our model maintains an exceptionally low FP rate ($5 / 904 = 0.55\%$).

---

## 8. Step-by-Step Installation & Run Guide (Windows / VS Code)

### Step 1: Open Terminal in VS Code
Open VS Code, press `Ctrl + ~` to open the integrated PowerShell terminal, and navigate to the project directory:

```powershell
cd "C:\Users\Ajan\.gemini\antigravity\scratch\EmailSpamDetection"
```

### Step 2: Create and Activate Virtual Environment (Recommended)
```powershell
# Create virtual environment named venv
python -m venv venv

# Activate virtual environment on Windows PowerShell
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### Step 3: Install Required Libraries
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Training Script
Train the machine learning model, compute genuine evaluation metrics, and generate all EDA plots:

```powershell
python train_model.py
```

*Expected output:*
```text
=================================================================
 Email Spam Detection Using Machine Learning & Naive Bayes
 Complete College Mini-Project Training Workflow
=================================================================
[1/10] Found existing dataset at: data/spam.csv
[2/10] Loading and inspecting raw dataset...
       Cleaned dataset dimensions: 5158 rows, 4 columns
       Class distribution: Ham = 4516 (87.55%), Spam = 642 (12.45%)
[3/10] Generating Exploratory Data Analysis (EDA) visualizations...
       Saved 5 EDA plots to static/plots/
[4/10] Splitting dataset into 80% Train and 20% Test (stratified)...
[5/10] Comparing Text Feature Extractors (CountVectorizer vs TfidfVectorizer)...
[6/10] Building final Scikit-learn Pipeline (CountVectorizer + MultinomialNB)...
[7/10] Fitting pipeline strictly on training data...
[8/10] Evaluating model on held-out test data...
  Test Accuracy:    98.35%
  Spam Precision:   95.87%
  Spam Recall:      90.62%
  Spam F1-Score:    93.17%
[9/10] Generating Confusion Matrix Visualization...
[10/10] Saving model pipeline and evaluation report...
=================================================================
```

### Step 5: Start the Flask Web Application
```powershell
python app.py
```

*Expected output:*
```text
=================================================================
 Starting Email Spam Detection Web Application...
 Open your browser and navigate to: http://127.0.0.1:5000
 Press Ctrl+C in the terminal to stop the server.
=================================================================
 * Running on http://127.0.0.1:5000
```

### Step 6: Open the Web Application
Open your web browser (Chrome, Edge, or Firefox) and navigate to:
```text
http://127.0.0.1:5000
```

---

## 9. How to Test the Application

### Testing Spam Messages
1. In the input box, paste:
   ```text
   Congratulations! You have won a $1,000 Walmart Gift Card. Claim now by calling 0800123456 or visit http://claim-prize.example.com!
   ```
2. Click **Predict Message**.
3. **Observed Output:**
   - Badge: `🚨 SPAM DETECTED`
   - Spam Probability: `~99.8%`
   - Ham Probability: `~0.2%`

### Testing Legitimate (Ham) Messages
1. In the input box, paste:
   ```text
   Hi, are you coming to college tomorrow? Let's finish the database and machine learning lab assignments together.
   ```
2. Click **Predict Message**.
3. **Observed Output:**
   - Badge: `✅ NOT SPAM (HAM)`
   - Spam Probability: `~0.01%`
   - Ham Probability: `~99.99%`

### Testing Edge Cases
- **Empty input:** Displays a validation alert asking the user to provide message content.
- **Clear button:** Clears the input field and resets focus immediately.

---

## 10. College Demonstration Checklist (Screenshots Guide)

When presenting this mini-project to college examiners or in a viva, capture screenshots of the following 8 areas:

1. **Dataset Collection:** Section showing total samples (5,158), Ham (4,516), and Spam (642) with first 5 rows preview.
2. **Data Preprocessing:** Summary metrics showing missing value cleaning, deduplication, and column standardization.
3. **EDA Visualizations:**
   - Spam vs Ham distribution bar plot
   - Message length comparison showing spam messages are substantially longer
   - Top 15 frequent spam keywords (`free`, `claim`, `call`, `txt`, `prize`) vs ham keywords (`ok`, `will`, `come`)
4. **Feature Extraction:** Explanation box showing CountVectorizer vs TF-IDF cross-validation comparison.
5. **Model Training:** Stratified 80/20 train-test split summary and pipeline architecture.
6. **Model Evaluation:** Metric cards showing **98.35% Accuracy**, **95.87% Precision**, and the Confusion Matrix heatmap.
7. **Spam Message Prediction:** Live classification showing red alert pill and model-estimated probabilities.
8. **Ham Message Prediction:** Live classification showing green success pill and model-estimated probabilities.

---

## 11. Common Errors and Troubleshooting

| Issue / Error | Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed in active environment | Run `pip install -r requirements.txt` in the terminal |
| `Model file not found at models/...` | Application started before running training script | Run `python train_model.py` first to generate model artifacts |
| `Address already in use (Port 5000)` | Another application is using port 5000 | In `app.py`, change `port=5000` to `port=5001` or run `Stop-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess -Force` |
| `ExecutionPolicy Error on Windows PowerShell` | Script execution disabled by default on Windows | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell |
| `UnicodeDecodeError` when loading dataset | File encoded in Latin-1 or CP1252 | Handled automatically by `train_model.py` which checks UTF-8, Latin-1, and CP1252 encodings |

---

## 12. Authors & License

- **Project:** Email Spam Detection Using Machine Learning & Naive Bayes
- **Curriculum:** B.Tech Information Technology (IT) Mini-Project
- **License:** Open Source under the MIT License
