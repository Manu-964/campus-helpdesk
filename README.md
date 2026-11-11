# 🎓 Presidency University – AI Campus Helpdesk

> **TECHNOPIA 2.0** | AI-Powered University Campus Helpdesk Challenge  
> School of Computer Science & Engineering, Presidency University  
> **Duration:** 60 Minutes (10:30 AM – 11:30 AM) | **Venue:** LG07

---

## 🚀 Overview

An **AI-Powered University Campus Helpdesk** portal designed for students of Presidency University. Students can query in natural language regarding academics, examinations, placements, hostel facilities, library rules, administrative procedures, and events, receiving prompt, accurate, and context-grounded responses extracted directly from the official **Presidency University Student Handbook 2025–2026**.

If a student's query falls outside the official supplied data (e.g., exact exam dates, unofficial rumours), the system explicitly and politely acknowledges the limitation without inventing facts or hallucinating.

---

## 🧠 AI Integration Details

| Dimension | Specification |
|-----------|---------------|
| **AI Model** | Google Gemini 3.8 Flash (`gemini-3.8-flash`) |
| **SDK** | Official Google GenAI SDK (`google-genai`) |
| **Grounding Source** | Official Presidency University Student Handbook 2025–26 & Competition Data |
| **Architecture** | Context-Grounded Prompting / RAG Pattern with Strict Hallucination Guardrails |
| **Security** | Zero frontend API key leakage; backend proxy via FastAPI with `.env` isolation |

### How AI is Integrated
1. **Natural Language Understanding:** Student inputs in natural, conversational phrasing are routed through the FastAPI `/api/chat` endpoint.
2. **Knowledge Retrieval & Grounding:** The prompt incorporates verified institutional policies across 8 core university domains:
   - **Academics:** CBCS curriculum, faculty advisor system, LMS access.
   - **Attendance:** Mandatory 75% requirement, impact on placement eligibility and hostel allocation.
   - **Examinations:** Official announcement channels, Examination Grievance Redressal Cell (`examredressal@presidencyuniversity.in`), provisional degree protocols.
   - **Placements & Internships:** Industry Interface and Placement Cell, 75% attendance threshold, disciplinary debarment rules.
   - **Library (LKRC):** 3 campus locations, 60,700+ books, Koha LMS/OPAC, Knimbus e-resources, 8:30 AM–6:30 PM working hours, borrowing & overdue rules (Rs. 5/10 per day).
   - **Hostel Facilities:** Separate boys/girls housing, first-come first-served, mandatory local guardian, 75% attendance rule.
   - **Administration & Services:** Bonafide certificates (1-day turnaround), transcripts, scholarship policy, fee payment/refund schedules.
   - **Student Affairs & Events:** 50+ clubs, NSS, NCC, Counselling Services, YourDOST partnership.
3. **Strict Truthfulness Guard:** The model is constrained to say *"I don't have that specific information. Please contact the relevant department or check the official university website at www.presidencyuniversity.in"* whenever details are not in the handbook (e.g. specific future exam dates or individual marks).

---

## 🛠️ Technology Stack

- **Backend:** Python 3, FastAPI, Uvicorn (ASGI server)
- **AI Engine:** Google GenAI (`gemini-3.8-flash`)
- **Frontend:** Responsive Portal UI (HTML5, Modern CSS3 Flex/Grid, Vanilla JavaScript)
- **Configuration:** Python-Dotenv for secure credential handling

---

## 📁 Repository Structure

```
campus-helpdesk/
├── main.py              # FastAPI server, endpoints & knowledge-base grounding
├── requirements.txt     # Python dependencies
├── .env                 # API key configuration (excluded via .gitignore)
├── .gitignore           # Ignores .env, caches, virtual environments
├── README.md            # Project documentation & runbook
└── static/
    └── index.html       # Full interactive Helpdesk UI & live chat client
```

---

## ⚡ Quickstart Guide

### 1. Clone & Enter Directory
```bash
git clone <repository-url>
cd campus-helpdesk
```

### 2. Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. API Key Configuration
Create or edit `.env` in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access Helpdesk
Open your browser and navigate to:
**http://localhost:8000** (or `http://127.0.0.1:8000`)

---

## 🧪 Verification & Test Cases

| Category | Test Question | Expected Output | Tested Result |
|----------|---------------|-----------------|---------------|
| **Academics** | *"Whom should I contact for academic problems?"* | Suggest contacting the faculty advisor / department office | ✅ Pass |
| **Examinations** | *"Where can I find the examination timetable?"* | Directs to official university channels / notice boards / website | ✅ Pass |
| **Placements** | *"Whom should I contact for placement training?"* | Suggests Placement Department / Industry Interface Cell | ✅ Pass |
| **Hostel** | *"How can I raise a hostel complaint?"* | Directs to Hostel Administration | ✅ Pass |
| **Unknown Fact** | *"What is the exact date of my next examination?"* | Honest statement of unavailability in handbook; no invented date | ✅ Pass |
| **Attendance** | *"What is the minimum attendance requirement?"* | Explains 75% rule and consequences on placement/hostel | ✅ Pass |
| **Library** | *"What are the library working hours?"* | Returns 8:30 AM to 6:30 PM (8:00 PM during exams) | ✅ Pass |
| **Admin** | *"How do I get a bonafide certificate?"* | Explains applying at Registrar's office (1-day issuance) | ✅ Pass |

---


Built for **TECHNOPIA 2.0** • School of Computer Science & Engineering • Presidency University
