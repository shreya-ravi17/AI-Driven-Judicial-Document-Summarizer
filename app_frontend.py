import streamlit as st
import os
from summarizer_backend import summarize_long_text, extract_text_pdf, extract_text_docx, load_model, translate_summary

# ----- Page Config -----
st.set_page_config(page_title="AI Summarizer", page_icon="✨", layout="centered")

# ----- STYLING -----
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #c7d2fe, #fbcfe8);
}

/* Header */
.header {
    text-align: center;
    padding: 10px;
}

.header h1 {
    font-size: 38px;
    color: #4c1d95;
}

.header p {
    color: #6d28d9;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    background: #e0e7ff;
    border-radius: 10px;
    padding: 10px 20px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    color: white;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    border: none;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background: linear-gradient(to right, #e0f2fe, #ede9fe);
    padding: 15px;
    border-radius: 12px;
    border: 2px dashed #a5b4fc;
}

/* Textarea */
textarea {
    border-radius: 10px !important;
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #111827 !important;
}
/* ===== DROPDOWN FIX ===== */
ul[role="listbox"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

li[role="option"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

li[role="option"]:hover {
    background-color: #e0e7ff !important;
}

li[aria-selected="true"] {
    background-color: #c7d2fe !important;
    color: #111827 !important;
}
/* ===== FILE UPLOADER FIX ===== */

/* Outer upload box */
[data-testid="stFileUploader"] {
    background: linear-gradient(to right, #e0f2fe, #ede9fe) !important;
    border: 2px dashed #818cf8 !important;
    border-radius: 12px;
    padding: 15px;
}

/* Inner drag box (remove black) */
[data-testid="stFileUploader"] section {
    background: #f8fafc !important;
    color: #1e293b !important;
    border-radius: 10px;
}

/* Drag text */
[data-testid="stFileUploader"] span {
    color: #1e293b !important;
    font-weight: 500;
}

/* "Browse files" button */
[data-testid="stFileUploader"] button {
    background: linear-gradient(to right, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 8px;
}

/* Small text (Upload PDF or DOCX) */
[data-testid="stFileUploader"] small {
    color: #475569 !important;
}
label {
    color: #6d28d9 !important;
}
/*  HEADING COLOR FIX  */
h1, h2, h3 {
    color: #4c1d95 !important;   /* same purple */
}
/*  CUSTOM SUCCESS BOX  */
.success-box {
    background: linear-gradient(to right, #eef2ff, #ede9fe);
    color: #4c1d95;
    padding: 12px 16px;
    border-radius: 10px;
    border-left: 6px solid #7c3aed;
    font-weight: 600;
    margin-top: 10px;
}
/*  SUMMARY BOX  */
.summary-box {
    background-color: #f9fafb !important;
    color: #111827 !important;
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid #4c1d95;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
    font-size: 16px;
    line-height: 1.6;
    margin-top: 12px;
}

/* TRANSLATED SUMMARY VARIANT  */
.translated-box {
    background-color: #eef2ff !important;
    border-left: 6px solid #6366f1;
}
            
</style>
""", unsafe_allow_html=True)

# ----- Load Model -----
@st.cache_resource
def load_cached_model():
    return load_model()

tokenizer, model = load_cached_model()

# ----- HEADER -----
st.markdown("""
<div class="header">
    <h1>✨ AI Judicial Summarizer</h1>
    <p>Summarize legal documents easily</p>
</div>
""", unsafe_allow_html=True)

# ----- TABS -----
tab1, tab2, tab3 = st.tabs(["✍️ Text", "📂 File", "⚙️ Settings"])

# ----- SETTINGS TAB -----
with tab3:
    st.subheader("🌐 Language Settings")

    language = st.selectbox(
        "Choose output language",
        ["English", "Hindi", "Kannada", "Tamil", "Telugu"]
    )

    lang_code_map = {
        "English": "en",
        "Hindi": "hi",
        "Kannada": "kn",
        "Tamil": "ta",
        "Telugu": "te"
    }

    selected_lang_code = lang_code_map[language]

# ----- TEXT TAB -----
with tab1:
    st.subheader("✍️ Enter Text to Summarize")

    user_text = st.text_area("Paste your text here:", height=250)

    if st.button("🚀 Summarize Text"):
        if user_text.strip():
            with st.spinner("Processing..."):
                summary = summarize_long_text(user_text, tokenizer, model)
                translated_summary = translate_summary(summary, selected_lang_code)

            st.markdown("""
            <div class="success-box">
            ✅ Summary Ready
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="summary-box">
            <b>🌐 Translated Summary:</b><br><br>
            {translated_summary}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please enter text")

# ----- FILE TAB -----
with tab2:
    st.subheader("📂 Upload Document")

    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]
        temp_file_path = f"temp_uploaded.{file_type}"

        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if file_type == "pdf":
            extracted_text = extract_text_pdf(temp_file_path)
        else:
            extracted_text = extract_text_docx(temp_file_path)

        if extracted_text.strip():
            st.text_area("Extracted Text", extracted_text, height=200)

            if st.button("📊 Summarize File"):
                with st.spinner("Processing..."):
                    summary = summarize_long_text(extracted_text, tokenizer, model)
                    translated_summary = translate_summary(summary, selected_lang_code)

                st.success("Summary Ready")
                st.write(translated_summary)
        else:
            st.error("Extraction failed")

        os.remove(temp_file_path)