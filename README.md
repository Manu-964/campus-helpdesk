# 🎓 Presidency University – AI Campus Helpdesk

> **TECHNOPIA 2.0** | AI-Powered University Campus Helpdesk Challenge  
> School of Computer Science & Engineering, Presidency University

---

## 🚀 Overview

An **AI-powered chatbot** that helps students at Presidency University get quick, accurate answers about campus services — academics, examinations, placements, library, hostel, administration, and events.

The assistant is grounded in official university information and **will not fabricate** facts it doesn't know, instead directing students to the right department.

---

## 🧠 AI Integration

| Component | Details |
|-----------|---------|
| **AI Model** | Google Gemini 1.5 Flash |
| **API** | Google Generative AI (`google-generativeai`) |
| **Approach** | Retrieval-Augmented Generation (RAG-style) — the LLM is given a structured university knowledge base as context and instructed to answer only from it |
| **Hallucination prevention** | System prompt explicitly instructs the model to say "I don't have that information" for queries outside the knowledge base |

### How AI is Integrated

1. The backend embeds a **structured knowledge base** (covering all 8 categories) in the system prompt.
2. The student's question is appended to this prompt and sent to **Gemini 1.5 Flash**.
3. Gemini generates a natural-language response grounded **only** in the provided information.
4. The FastAPI backend returns the response to the frontend — no API key is exposed to the browser.

---

## 🛠️ Tech Stack

- **Backend:** Python + [FastAPI](https://fastapi.tiangolo.com/)
- **AI:** [Google Gemini 1.5 Flash](https://ai.google.dev/) via `google-generativeai`
- **Frontend:** Vanilla HTML + CSS + JavaScript (served by FastAPI)
- **Config:** python-dotenv for secure API key management

---

## 📁 Project Structure

```
campus-helpdesk/
├── main.py              # FastAPI backend + Gemini integration
├── requirements.txt     # Python dependencies
├── .env                 # API key (not committed)
├── .gitignore
├── README.md
└── static/
    └── index.html       # Chat UI (responsive, Presidency University themed)
```

---

## ⚡ Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd campus-helpdesk
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get a free API key at: https://aistudio.google.com/app/apikey

### 5. Run the application
```bash
uvicorn main:app --reload
```

### 6. Open in browser
Navigate to: **http://localhost:8000**

---

## 💬 Sample Questions to Test

| Question | Expected Behaviour |
|----------|-------------------|
| Whom should I contact for academic problems? | Suggests faculty advisor |
| Where can I find the exam timetable? | Refers to official university channels |
| Whom should I contact for placement training? | Suggests Placement Department |
| How can I raise a hostel complaint? | Refers to Hostel Administration |
| What is the exact date of my next exam? | States that specific date is unavailable |
| How do I get a bonafide certificate? | Refers to administrative office |

---

## 🎨 Features

- ✅ Real-time AI chat interface
- ✅ Typing indicator animation
- ✅ 8 quick-access category cards
- ✅ Suggestion chips for common queries
- ✅ Topic badges in header for one-click questions
- ✅ Responsive design (mobile-friendly)
- ✅ Secure API key handling (server-side only)
- ✅ Honest unknown-query handling (no hallucination)
- ✅ Presidency University branded UI

---

## 🔒 Security

- The Gemini API key is stored in `.env` and loaded server-side only.
- The frontend never has access to the API key — all AI calls go through the `/api/chat` endpoint.

---

## 👥 Team

Built for **TECHNOPIA 2.0** – Build It in 60 Minutes  
Presidency University | School of Computer Science & Engineering

