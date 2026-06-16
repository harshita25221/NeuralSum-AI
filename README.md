# ⚡ NeuralSum AI - Intelligent Text Summarizer

## 📖 Project Overview

NeuralSum AI is an NLP-based Text Summarization application developed using Python and spaCy. The system automatically extracts the most important sentences from a document and generates a concise summary while preserving the original meaning.

The project supports PDF, DOCX, TXT, and manual text input. It also provides detailed analytics, keyword extraction, visualization dashboards, and PDF export functionality.

## 🎯 Objectives

* Reduce lengthy documents into concise summaries.
* Improve reading efficiency and save time.
* Demonstrate Natural Language Processing concepts.
* Provide document analytics through visualizations.
* Support multiple document formats.

## 🚀 Features

### 📄 Multi-Format Document Support

* PDF Upload
* DOCX Upload
* TXT Upload
* Manual Text Input

### 🧠 NLP-Based Summarization

* Tokenization
* Lemmatization
* Stop-word Removal
* Sentence Segmentation
* Frequency-Based Sentence Scoring
* Extractive Summarization

### 📊 Analytics Dashboard

* Original Word Count
* Summary Word Count
* Original Sentence Count
* Summary Sentence Count
* Compression Ratio
* Reading Time Estimation
* Time Saved Analysis

### 📈 Data Visualization

* Top Keywords Frequency Chart
* Original vs Summary Comparison
* Sentence Reduction Analysis
* Compression Ratio Pie Chart

### 📥 Export Options

* Download Summary as PDF
* Download Summary as TXT

### 🎨 User Interface

* Modern Streamlit Dashboard
* Responsive Design
* Interactive Controls
* Professional Analytics Cards

## 🏗️ System Architecture

User Input (PDF/DOCX/TXT/Text)

↓

Text Extraction

↓

spaCy NLP Processing

↓

Tokenization

↓

Stop-word Removal

↓

Lemmatization

↓

Word Frequency Calculation

↓

Sentence Scoring

↓

Summary Generation

↓

Analytics & Visualization

↓

PDF/TXT Export

## 🛠️ Technologies Used

### Python

Core programming language used for development.

### spaCy

Used for Natural Language Processing tasks:

* Tokenization
* Lemmatization
* Sentence Segmentation
* Stop-word Removal

### Streamlit

Used to build the web application interface.

### NumPy

Used for numerical computations.

### Matplotlib

Used for generating charts and visual analytics.

### PyPDF2

Used to extract text from PDF documents.

### python-docx

Used to read text from DOCX files.

### ReportLab

Used to generate downloadable PDF reports.

## 📂 Project Structure

```text
Text_Summarizer_Project/
│
├── app.py
├── summarizer.py
├── requirements.txt
├── README.md
│
├── assets/
│
└── sample_documents/
```

## ⚙️ Installation

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Text_Summarizer_Project
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### Step 6: Run Application

```bash
streamlit run app.py
```

---

## 📦 Required Libraries

```text
spacy
numpy
streamlit
matplotlib
PyPDF2
python-docx
reportlab
```

## 🧪 Working Methodology

### 1. Input Collection

The user uploads a document or enters text manually.

### 2. Text Preprocessing

spaCy processes the text and performs:

* Tokenization
* Lemmatization
* Stop-word Removal

### 3. Frequency Analysis

Important words are identified based on frequency.

### 4. Sentence Scoring

Each sentence receives a score based on important word occurrences.

### 5. Summary Generation

Top-ranked sentences are selected to generate the summary.

### 6. Analytics Generation

Word counts, sentence counts, compression ratio, and reading time are calculated.

### 7. Visualization

Graphs and charts are generated using Matplotlib.

### 8. Export

Summary can be downloaded as PDF or TXT.

## 📊 Sample Output Metrics

* Original Words: 1200
* Summary Words: 350
* Compression Ratio: 70%
* Reading Time Saved: 5 Minutes

## 🎓 Educational Concepts Demonstrated

* Natural Language Processing (NLP)
* Text Preprocessing
* Extractive Text Summarization
* Frequency-Based Ranking
* Data Visualization
* Document Processing
* Web Application Development

## 🔮 Future Enhancements

* Abstractive Summarization using Transformers
* Multilingual Summarization
* Text-to-Speech Summary
* Keyword Cloud Visualization
* AI-Powered Chat with Documents
* OCR Support for Scanned PDFs
* Summarization API Integration

## 👨‍💻 Conclusion

NeuralSum AI provides an efficient solution for automatically summarizing large documents using Natural Language Processing techniques. The system improves productivity, reduces reading time, and presents meaningful insights through interactive analytics and visualizations.

### Developed Using

🐍 Python | 🧠 spaCy | ⚡ Streamlit | 📊 Matplotlib | 📄 PyPDF2 | 📝 python-docx | 📥 ReportLab
