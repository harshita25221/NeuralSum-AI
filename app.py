# this file created the streamlit interface for the user to interact with the summarizer
import streamlit as st 
import PyPDF2
import docx
import matplotlib.pyplot as plt 
import io # The io module is used for handling files in memory without saving them permanently on your computer.
from datetime import datetime # The datetime module is used to work with dates and times in Python. It provides classes for manipulating dates and times, including formatting, parsing, and arithmetic operations.
from summarizer import (
    summarize_text,
    get_word_frequencies,
    get_top_keywords,
    get_text_statistics,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
) # The reportlab library is used to generate PDF reports in Python. It provides a high-level interface for creating complex documents with text, images, tables, and other elements. The specific classes imported from reportlab are used to create a PDF document, define styles for paragraphs, and create tables with custom styling.
st.set_page_config(
    page_title="AI | Intelligent Text Summarizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
) # The set_page_config function is used to configure the layout and appearance of the Streamlit app. It sets the page title, page icon, layout style, and initial state of the sidebar. This function should be called at the beginning of the script before any other Streamlit commands.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
 
    html, body, [class*="css"] {
        font-family: 'Inter', 'Poppins', sans-serif;
    }
 
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #0d1333 35%, #131a40 70%, #0a0e27 100%);
        color: #ffffff;
    }
 
    /* Hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
 
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, rgba(0, 198, 255, 0.15) 0%, rgba(124, 58, 237, 0.2) 50%, rgba(0, 198, 255, 0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px 50px;
        margin-bottom: 30px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 198, 255, 0.15);
        text-align: center;
        animation: fadeInDown 0.8s ease;
    }
 
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(90deg, #00c6ff, #7c3aed, #00f5d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
 
    .hero-subtitle {
        font-size: 18px;
        color: #b8c1ec;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 20px auto;
        line-height: 1.6;
    }
 
    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #00c6ff, #7c3aed);
        color: white;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px 6px;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
        animation: pulse 2s infinite;
    }
 
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4); }
        50% { box-shadow: 0 4px 25px rgba(0, 198, 255, 0.6); }
        100% { box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4); }
    }
 
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
 
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
 
    /* Premium Cards (glassmorphism) */
    .premium-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 25px 28px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease;
    }
 
    .premium-card:hover {
        border: 1px solid rgba(0, 198, 255, 0.3);
        box-shadow: 0 8px 40px rgba(0, 198, 255, 0.2);
        transform: translateY(-2px);
    }
 
    .card-title {
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(90deg, #00c6ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 15px;
    }
 
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1333 0%, #131a40 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
 
    section[data-testid="stSidebar"] .premium-card {
        background: rgba(255, 255, 255, 0.03);
    }
 
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 28px;
        font-size: 17px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.35);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
 
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 30px rgba(0, 198, 255, 0.5);
        color: white;
        border: none;
    }
 
    .stDownloadButton > button {
        background: linear-gradient(90deg, #00f5d4 0%, #00c6ff 100%);
        color: #0a0e27;
        border: none;
        border-radius: 14px;
        padding: 12px 24px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 6px 20px rgba(0, 245, 212, 0.3);
        transition: all 0.3s ease;
    }
 
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 245, 212, 0.5);
    }
 
    /* KPI Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
 
    div[data-testid="stMetric"]:hover {
        border: 1px solid rgba(0, 198, 255, 0.35);
        transform: translateY(-3px);
    }
 
    div[data-testid="stMetricValue"] {
        color: #00f5d4;
        font-weight: 800;
    }
 
    div[data-testid="stMetricLabel"] {
        color: #b8c1ec;
        font-weight: 600;
    }
 
    /* Keyword pills/chips */
    .keyword-chip {
        display: inline-block;
        background: linear-gradient(90deg, rgba(0, 198, 255, 0.2), rgba(124, 58, 237, 0.25));
        border: 1px solid rgba(0, 198, 255, 0.4);
        color: #e0f7ff;
        padding: 8px 18px;
        border-radius: 50px;
        margin: 5px;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.25s ease;
    }
 
    .keyword-chip:hover {
        background: linear-gradient(90deg, rgba(0, 198, 255, 0.4), rgba(124, 58, 237, 0.45));
        transform: scale(1.07);
    }
 
    /* Upload area */
    .upload-info {
        background: rgba(0, 198, 255, 0.08);
        border: 1px dashed rgba(0, 198, 255, 0.4);
        border-radius: 14px;
        padding: 15px 20px;
        margin-top: 10px;
        animation: fadeIn 0.5s ease;
    }
 
    .success-banner {
        background: linear-gradient(90deg, rgba(0, 245, 212, 0.15), rgba(0, 198, 255, 0.15));
        border: 1px solid rgba(0, 245, 212, 0.4);
        border-radius: 14px;
        padding: 14px 20px;
        color: #00f5d4;
        font-weight: 600;
        margin-top: 10px;
        animation: fadeIn 0.5s ease;
    }
 
    /* Summary text box */
    .summary-box {
        background: rgba(255, 255, 255, 0.04);
        border-left: 4px solid #00c6ff;
        border-radius: 12px;
        padding: 22px 26px;
        font-size: 16.5px;
        line-height: 1.8;
        color: #e8edff;
        margin-top: 10px;
    }
 
    /* Section headers */
    .section-header {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin: 30px 0 15px 0;
        border-left: 4px solid #00c6ff;
        padding-left: 14px;
        background: linear-gradient(90deg, #ffffff, #b8c1ec);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
 
    /* Footer */
    .footer-container {
        background: rgba(255, 255, 255, 0.03);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px 18px 0 0;
        padding: 30px;
        text-align: center;
        margin-top: 50px;
        color: #b8c1ec;
    }
 
    .footer-tech {
        display: inline-block;
        background: rgba(0, 198, 255, 0.1);
        border: 1px solid rgba(0, 198, 255, 0.25);
        padding: 6px 16px;
        border-radius: 50px;
        margin: 4px;
        font-size: 13px;
        font-weight: 600;
        color: #e0f7ff;
    }
 
    /* Text areas / inputs */
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
 
    /* Sliders */
    .stSlider [data-baseweb="slider"] {
        margin-top: 10px;
    }
 
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00c6ff, #7c3aed) !important;
    }
 
    /* Quality indicator badges */
    .quality-badge {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
 
    .quality-badge:hover {
        border: 1px solid rgba(124, 58, 237, 0.4);
        transform: translateY(-2px);
    }
 
    .quality-value {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #00c6ff, #00f5d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
 
    .quality-label {
        font-size: 13px;
        color: #b8c1ec;
        font-weight: 600;
        margin-top: 5px;
    }
     /* ============================================================
       MOBILE RESPONSIVE OVERRIDES
       ============================================================ */
    @media (max-width: 768px) {
        .hero-container {
            padding: 25px 20px;
            border-radius: 18px;
        }
 
        .hero-title {
            font-size: 32px;
            letter-spacing: -0.5px;
        }
 
        .hero-subtitle {
            font-size: 15px;
            padding: 0 5px;
        }
 
        .badge {
            font-size: 11px;
            padding: 5px 12px;
            margin: 3px 3px;
        }
 
        .premium-card {
            padding: 16px 18px;
            border-radius: 14px;
        }
 
        .card-title {
            font-size: 17px;
        }
 
        .section-header {
            font-size: 20px;
            margin: 20px 0 10px 0;
            padding-left: 10px;
        }
 
        .summary-box {
            padding: 16px 18px;
            font-size: 15px;
            line-height: 1.7;
        }
 
        .keyword-chip {
            font-size: 12px;
            padding: 6px 12px;
            margin: 3px;
        }
 
        .quality-value {
            font-size: 22px;
        }
 
        .quality-label {
            font-size: 11px;
        }
 
        div[data-testid="stMetricValue"] {
            font-size: 22px;
        }
 
        .footer-container {
            padding: 20px 15px;
        }
 
        .footer-tech {
            font-size: 11px;
            padding: 5px 12px;
            margin: 3px;
        }
        }
    </style>
    """,
    unsafe_allow_html=True,
)
def extract_text_from_pdf(file) -> str:
    """Extract text content from an uploaded PDF file."""
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()
 
 
def extract_text_from_docx(file) -> str:
    """Extract text content from an uploaded DOCX file."""
    document = docx.Document(file)
    text = "\n".join([para.text for para in document.paragraphs])
    return text.strip()
 
 
def extract_text_from_txt(file) -> str:
    """Extract text content from an uploaded TXT file."""
    return file.read().decode("utf-8", errors="ignore").strip()
 
 
def estimate_reading_time(word_count, wpm=200) -> float:
    """Return estimated reading time in minutes based on word count."""
    return round(word_count / wpm, 2)
 
 
def generate_pdf_report(original_text, summary, stats, keywords) -> bytes:
    """Generate a downloadable PDF report of the summary using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
 
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        textColor=colors.HexColor("#7c3aed"),
        fontSize=24,
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#00538c"),
        spaceBefore=12,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        leading=18,
        spaceAfter=10,
    )
 
    elements = []
 
    elements.append(Paragraph("⚡ NeuralSum AI - Summary Report", title_style))
    elements.append(Spacer(1, 12))
    elements.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            body_style,
        )
    )
    elements.append(Spacer(1, 12))
 
    elements.append(Paragraph("Generated Summary", heading_style))
    elements.append(Paragraph(summary.replace("\n", "<br/>"), body_style))
    elements.append(Spacer(1, 12))
 
    elements.append(Paragraph("Document Statistics", heading_style))
    table_data = [
        ["Metric", "Value"],
        ["Original Words", str(stats["original_words"])],
        ["Summary Words", str(stats["summary_words"])],
        ["Original Sentences", str(stats["original_sentences"])],
        ["Summary Sentences", str(stats["summary_sentences"])],
        ["Compression Ratio", f"{stats['compression_ratio']}%"],
    ]
    table = Table(table_data, colWidths=[8 * cm, 8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00c6ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    elements.append(table)
    elements.append(Spacer(1, 12))
 
    elements.append(Paragraph("Top Keywords", heading_style))
    keyword_str = ", ".join([f"{word} ({count})" for word, count in keywords])
    elements.append(Paragraph(keyword_str, body_style))
 
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "stats" not in st.session_state:
    st.session_state.stats = None
if "keywords" not in st.session_state:
    st.session_state.keywords = None
if "word_freq" not in st.session_state:
    st.session_state.word_freq = None
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚡ NeuralSum AI</div>
        <div class="hero-subtitle">
            Transform lengthy documents into concise, intelligent summaries using
            Natural Language Processing.
        </div>
        <div>
            <span class="badge">🧠 Powered by spaCy NLP</span>
            <span class="badge">⚡ Extractive Summarization</span>
            <span class="badge">📊 Real-time Analytics</span>
            <span class="badge">📥 PDF Export Ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)   
with st.sidebar:
    st.markdown(
        """
        <div class="premium-card">
            <div class="card-title">📊 Project Overview</div>
            <p style="color:#b8c1ec; font-size:14px; line-height:1.6;">
            NeuralSum AI is an intelligent text summarization platform that uses
            Natural Language Processing to extract the most important sentences
            from any document, providing concise summaries with full analytics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    st.markdown(
        """
        <div class="premium-card">
            <div class="card-title">⚙️ Controls</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    summary_percentage = st.select_slider(
        "📏 Summary Length",
        options=[10, 20, 30, 40, 50, 60, 70, 80],
        value=30,
        help="Select what percentage of the original text should remain in the summary.",
    )
 
    st.markdown(
        f"""
        <div class="upload-info" style="text-align:center;">
            <span style="font-size:22px; font-weight:800; color:#00f5d4;">{summary_percentage}%</span>
            <br>
            <span style="font-size:13px; color:#b8c1ec;">of original text retained</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    st.markdown(
        """
        <div class="premium-card" style="margin-top:20px;">
            <div class="card-title" style="font-size:17px;">ℹ️ System Information</div>
            <p style="color:#e0f7ff; font-size:14px; line-height:2;">
                🧠 <b>NLP Engine:</b> spaCy<br>
                ✂️ <b>Summarization Type:</b> Extractive<br>
                📊 <b>Analytics:</b> Enabled<br>
                📥 <b>PDF Export:</b> Enabled
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown('<div class="section-header">📤 Upload Your Document</div>', unsafe_allow_html=True)
 
st.markdown(
    """
    <div class="premium-card">
        <p style="color:#b8c1ec; font-size:14px;">
        Drag and drop a file below, or click to browse. Supported formats:
        <b>📄 PDF</b>, <b>📝 DOCX</b>, <b>📃 TXT</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "txt"],
    label_visibility="collapsed",
)
 
if uploaded_file is not None:
    try:
        with st.spinner("🔍 Extracting text from your document..."):
            file_type = uploaded_file.name.split(".")[-1].lower()
 
            if file_type == "pdf":
                extracted = extract_text_from_pdf(uploaded_file)
                file_icon = "📄"
            elif file_type == "docx":
                extracted = extract_text_from_docx(uploaded_file)
                file_icon = "📝"
            elif file_type == "txt":
                extracted = extract_text_from_txt(uploaded_file)
                file_icon = "📃"
            else:
                extracted = ""
                file_icon = "❓"
 
        if extracted:
            st.session_state.extracted_text = extracted
            st.session_state.text_input_area = extracted
            st.markdown(
                f"""
                <div class="success-banner">
                    ✅ Successfully extracted text from <b>{file_icon} {uploaded_file.name}</b>
                    ({len(extracted.split())} words detected)
                </div>
                """,
                unsafe_allow_html=True,
            )
 
            with st.expander("📖 View Extracted Text", expanded=False):
                st.markdown(
                    f'<div class="summary-box">{extracted[:3000]}'
                    f'{"..." if len(extracted) > 3000 else ""}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.warning("⚠️ No text could be extracted from this file. Please try another document.")
 
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
st.markdown('<div class="section-header">✍️ Or Enter Text Manually</div>', unsafe_allow_html=True)
 
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
 
if "text_input_area" not in st.session_state:
    st.session_state.text_input_area = ""

if st.session_state.extracted_text:
    st.session_state.text_input_area = st.session_state.extracted_text

input_text = st.text_area(
    "Enter or paste your text here",
    height=250,
    placeholder="Paste your article, report, or document text here...",
    label_visibility="collapsed",
    key="text_input_area",
)
# Live counters
char_count = len(input_text)
word_count = len(input_text.split()) if input_text.strip() else 0
sentence_count = input_text.count(".") + input_text.count("!") + input_text.count("?")
 
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="quality-badge">
            <div class="quality-value">{char_count}</div>
            <div class="quality-label">🔤 Characters</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
        <div class="quality-badge">
            <div class="quality-value">{word_count}</div>
            <div class="quality-label">📝 Words</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
        <div class="quality-badge">
            <div class="quality-value">{sentence_count}</div>
            <div class="quality-label">📚 Sentences (approx.)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
generate_clicked = st.button("🚀 Generate Intelligent Summary", use_container_width=True)
 
if generate_clicked:
    if not input_text.strip():
        st.warning("⚠️ Please upload a document or enter some text before generating a summary.")
    else:
        try:
            with st.spinner("🧠 Analyzing text and generating intelligent summary..."):
                percentage_fraction = summary_percentage / 100
                summary = summarize_text(input_text, percentage_fraction)
                stats = get_text_statistics(input_text, summary)
                keywords = get_top_keywords(input_text, n=10)
                word_freq = get_word_frequencies(input_text)
 
            st.session_state.summary = summary
            st.session_state.stats = stats
            st.session_state.keywords = keywords
            st.session_state.word_freq = word_freq
 
            st.markdown(
                """
                <div class="success-banner">
                    ✅ Summary generated successfully! Scroll down to view your results.
                </div>
                """,
                unsafe_allow_html=True,
            )
 
        except Exception as e:
            st.error(f"❌ An error occurred while generating the summary: {str(e)}")
if st.session_state.summary and st.session_state.stats:
    summary = st.session_state.summary
    stats = st.session_state.stats
    keywords = st.session_state.keywords
    word_freq = st.session_state.word_freq

    st.markdown('<div class="section-header">✨ Generated Summary</div>', unsafe_allow_html=True)
    summary_word_count = stats["summary_words"]
    summary_reading_time = estimate_reading_time(summary_word_count)

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="summary-box">{summary}</div>
            <br>
            <span class="keyword-chip">📝 {summary_word_count} words</span>
            <span class="keyword-chip">⏱ {summary_reading_time} min read</span>
            <span class="keyword-chip">⚡ {stats['compression_ratio']}% compressed</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Copy to clipboard
   # 1. Import the components module at the top of your script or right here
    import streamlit.components.v1 as components

    # 2. Define the copy button HTML
    copy_html = f"""
    <div style="background-color: transparent;">
        <textarea id="summaryText" style="position:absolute; left:-9999px;">{summary}</textarea>
        <button onclick="navigator.clipboard.writeText(document.getElementById('summaryText').value);
            this.innerText='✅ Copied!'; setTimeout(()=>this.innerText='📋 Copy Summary to Clipboard', 2000);"
            style="background: linear-gradient(90deg, #00c6ff, #7c3aed); color:white; border:none;
            border-radius:12px; padding:10px 22px; font-weight:700; cursor:pointer; margin-top:10px;
            box-shadow: 0 4px 15px rgba(124,58,237,0.4); font-family: sans-serif;">
            📋 Copy Summary to Clipboard
        </button>
    </div>
    """
    
    # 3. Render it using the dedicated HTML component instead of st.markdown
    components.html(copy_html, height=70)

    # --------------------------------------------------------
    # KPI METRIC CARDS
    # --------------------------------------------------------
    st.markdown('<div class="section-header">📊 Summary Analytics</div>', unsafe_allow_html=True)

    original_reading_time = estimate_reading_time(stats["original_words"])
    time_saved = round(original_reading_time - summary_reading_time, 2)

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("📄 Original Words", stats["original_words"])
    with k2:
        st.metric("📝 Summary Words", stats["summary_words"])
    with k3:
        st.metric("⚡ Compression Ratio", f"{stats['compression_ratio']}%")

    k4, k5, k6 = st.columns(3)
    with k4:
        st.metric("📚 Original Sentences", stats["original_sentences"])
    with k5:
        st.metric("📋 Summary Sentences", stats["summary_sentences"])
    with k6:
        st.metric("⏱ Reading Time Saved", f"{time_saved} min")

    # --------------------------------------------------------
    # READING TIME ESTIMATION
    # --------------------------------------------------------
    st.markdown('<div class="section-header">⏱ Reading Time Estimation</div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(
            f"""
            <div class="quality-badge">
                <div class="quality-value">{original_reading_time} min</div>
                <div class="quality-label">📖 Original Reading Time</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            f"""
            <div class="quality-badge">
                <div class="quality-value">{summary_reading_time} min</div>
                <div class="quality-label">⚡ Summary Reading Time</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r3:
        st.markdown(
            f"""
            <div class="quality-badge">
                <div class="quality-value">{time_saved} min</div>
                <div class="quality-label">⏱ Time Saved</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # COMPRESSION PROGRESS BAR
    # --------------------------------------------------------
    st.markdown('<div class="section-header">📉 Compression Progress</div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#b8c1ec;'>Your document was compressed by <b style='color:#00f5d4;'>{stats['compression_ratio']}%</b></p>",
        unsafe_allow_html=True,
    )
    st.progress(min(max(stats["compression_ratio"] / 100, 0.0), 1.0))
    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SUMMARY QUALITY INDICATORS
    # --------------------------------------------------------
    st.markdown('<div class="section-header">🏆 Summary Quality Indicators</div>', unsafe_allow_html=True)

    information_retained = round(100 - stats["compression_ratio"], 2)
    compression_efficiency = stats["compression_ratio"]
    document_reduction = round(
        ((stats["original_sentences"] - stats["summary_sentences"]) / stats["original_sentences"]) * 100,
        2,
    ) if stats["original_sentences"] > 0 else 0

    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown(
            f"""
            <div class="quality-badge">
                <div class="quality-value">{information_retained}%</div>
                <div class="quality-label">🧩 Information Retained</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with q2:
        st.markdown(
            f"""
            <div class="quality-badge">
                <div class="quality-value">{compression_efficiency}%</div>
                <div class="quality-label">⚡ Compression Efficiency</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with q3:
        st.markdown(
            f"""
            <div class="quality-badge">
                <div class="quality-value">{document_reduction}%</div>
                <div class="quality-label">📉 Document Reduction</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # CHARTS SECTION
    # --------------------------------------------------------
    st.markdown('<div class="section-header">📈 Visual Analytics</div>', unsafe_allow_html=True)

    # Configure matplotlib for dark theme
    plt.rcParams.update(
        {
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "axes.edgecolor": "#b8c1ec",
            "axes.labelcolor": "#ffffff",
            "xtick.color": "#b8c1ec",
            "ytick.color": "#b8c1ec",
            "text.color": "#ffffff",
            "axes.titlecolor": "#ffffff",
            "font.size": 10,
        }
    )

    chart_col1, chart_col2 = st.columns(2)

    # Top Keywords Bar Chart
    with chart_col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("##### 📈 Top 10 Important Keywords")
        top10 = word_freq.most_common(10)
        if top10:
            words = [w for w, _ in top10]
            freqs = [f for _, f in top10]
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.barh(words[::-1], freqs[::-1], color="#00c6ff")
            ax.set_xlabel("Frequency")
            ax.set_title("Top 10 Important Keywords")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # Original vs Summary Word Count
    with chart_col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("##### 📊 Original vs Summary (Words)")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(
            ["Original Words", "Summary Words"],
            [stats["original_words"], stats["summary_words"]],
            color=["#7c3aed", "#00f5d4"],
        )
        ax.set_ylabel("Word Count")
        ax.set_title("Original vs Summary Comparison")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    chart_col3, chart_col4 = st.columns(2)

    # Sentence Reduction Analysis
    with chart_col3:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("##### ✂️ Sentence Reduction Analysis")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(
            ["Original Sentences", "Summary Sentences"],
            [stats["original_sentences"], stats["summary_sentences"]],
            color=["#00c6ff", "#7c3aed"],
        )
        ax.set_ylabel("Sentence Count")
        ax.set_title("Sentence Reduction Analysis")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # Compression Pie Chart
    with chart_col4:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("##### 🥧 Compression Analysis")
        removed_portion = max(stats["original_words"] - stats["summary_words"], 0)
        summary_portion = stats["summary_words"]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            [summary_portion, removed_portion],
            labels=["Summary Portion", "Removed Portion"],
            autopct="%1.1f%%",
            colors=["#00f5d4", "#7c3aed"],
            textprops={"color": "#ffffff"},
            startangle=90,
        )
        ax.set_title("Compression Analysis")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # TOP KEYWORDS AS CHIPS
    # --------------------------------------------------------
    st.markdown('<div class="section-header">🔑 Top Keywords</div>', unsafe_allow_html=True)

    chips_html = "".join(
        [f'<span class="keyword-chip">{word} ({count})</span>' for word, count in keywords]
    )
    st.markdown(f'<div class="premium-card">{chips_html}</div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # PDF DOWNLOAD
    # --------------------------------------------------------
    st.markdown('<div class="section-header">📥 Export Report</div>', unsafe_allow_html=True)

    try:
        pdf_bytes = generate_pdf_report(
    st.session_state.extracted_text,
    summary,
    stats,
    keywords
)
        st.download_button(
            label="📥 Download Summary as PDF",
            data=pdf_bytes,
            file_name="Summary_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"❌ Error generating PDF: {str(e)}")


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer-container">
        <p style="font-size:16px; font-weight:600; color:#ffffff;">⚡ NeuralSum AI</p>
        <p>Built with:</p>
        <div>
            <span class="footer-tech">🐍 Python</span>
            <span class="footer-tech">🧠 spaCy</span>
            <span class="footer-tech">📊 Matplotlib</span>
            <span class="footer-tech">⚡ Streamlit</span>
            <span class="footer-tech">📄 PyPDF2</span>
            <span class="footer-tech">📝 python-docx</span>
            <span class="footer-tech">📥 ReportLab</span>
        </div>
        <p style="margin-top:15px; font-size:13px; color:#7c8bb5;">
            © 2026 NeuralSum AI. Final-Year NLP Project. All Rights Reserved.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
