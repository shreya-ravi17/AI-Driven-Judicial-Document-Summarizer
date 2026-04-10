# ⚖️ AI Judicial Document Summarizer

✨ An AI-powered web application that summarizes lengthy legal/judicial documents and translates them into multiple regional languages using advanced NLP models.

---

## 📌 Overview

Legal documents are often long, complex, and difficult to understand.
This project simplifies legal text by generating concise summaries and translating them into regional languages for better accessibility.

---

## 🚀 Features

* 🧠 **Abstractive Summarization** using BART (`facebook/bart-large-cnn`)
* 📄 Supports **PDF & DOCX file uploads**
* ✍️ Direct **text input summarization**
* 🌐 **Multilingual Translation**:

  * English
  * Hindi
  * Kannada
  * Tamil
  * Telugu
* ⚡ Handles **long documents** using chunk-based summarization
* 🎨 Clean and modern UI using Streamlit

---

## 🛠️ Tech Stack

### 💻 Frontend

* Streamlit (UI + Styling)

### 🧠 Backend / AI

* Python
* HuggingFace Transformers
* BART Model (Summarization)
* NLLB & Helsinki Models (Translation)

### 📂 File Processing

* PyMuPDF (PDF extraction)
* python-docx (DOCX extraction)

---

## 🧠 How It Works

1. 📥 User inputs text or uploads a document
2. 🧹 Text is preprocessed and split into chunks
3. 🤖 BART model generates summaries for each chunk
4. 🔗 Summaries are combined into final output
5. 🌐 Optional translation into selected language
6. 📤 Clean summarized result displayed

---

## 📷 UI Preview

(Add screenshots here)

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/your-username/ai-judicial-summarizer.git

cd ai-judicial-summarizer

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📊 Example Output

### Input:

"Long legal judgment..."

### Output:

"Concise summary of the judgment highlighting key decisions and facts."

---

## 🌍 Supported Languages

* 🇬🇧 English
* 🇮🇳 Hindi
* 🇮🇳 Kannada
* 🇮🇳 Tamil
* 🇮🇳 Telugu

---

## 🔮 Future Enhancements

* 🔊 Voice output (Text-to-Speech)
* 📑 Legal entity extraction (judges, case numbers)
* 🔍 Keyword highlighting
* 🤖 Chatbot for legal queries
* 🌍 More language support

---

## 🎯 Use Cases

* 👩‍⚖️ Legal professionals
* 📚 Law students
* 🏛️ Judiciary systems
* 🔬 Legal research

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests!

---

## 📫 Contact

* LinkedIn: https://linkedin.com/in/shreyamashelkar7
* Email: [shreyamashelkar1712@gmail.com](mailto:shreyamashelkar1712@gmail.com)

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

---
