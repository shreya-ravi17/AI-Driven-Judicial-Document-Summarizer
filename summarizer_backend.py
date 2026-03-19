from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from docx import Document
import fitz  # PyMuPDF
import torch

def load_model():
    print("Loading English summarization model (BART)...")
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.eval()
    print("BART model loaded successfully ✅")
    return tokenizer, model

def summarize_text(text, tokenizer, model, max_length=150):
    if not text.strip():
        return "No text provided."

    with torch.no_grad():
        inputs = tokenizer([text], max_length=1024, truncation=True, return_tensors="pt")
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def summarize_long_text(text, tokenizer, model, chunk_size=500, max_length=150):
    words = text.split()
    chunk_summaries = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunk_summary = summarize_text(chunk, tokenizer, model, max_length)
        chunk_summaries.append(chunk_summary)

    if len(chunk_summaries) > 1:
        combined_summary_text = " ".join(chunk_summaries)
        final_summary = summarize_text(combined_summary_text, tokenizer, model, max_length)
    else:
        final_summary = chunk_summaries[0]

    return final_summary

def translate_summary(summary, target_lang):
    if target_lang == "en":
        return summary

    try:
        if target_lang == "kn":
            translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", src_lang="eng_Latn", tgt_lang="kan_Knda")
        elif target_lang == "hi":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
        elif target_lang == "ta":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ta")
        elif target_lang == "te":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-te")
        else:
            return summary
        translated = translator(summary)[0]["translation_text"]
        return translated
    except Exception as e:
        return f"[Translation failed: {e}]\n\n{summary}"

def extract_text_pdf(file_path):
    text = ""
    try:
        pdf_doc = fitz.open(file_path)
        for page in pdf_doc:
            text += page.get_text("text") + "\n"
        pdf_doc.close()
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

def extract_text_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"Error reading DOCX: {e}"
    return text