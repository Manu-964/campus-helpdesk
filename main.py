import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Campus Helpdesk API")

# Configure Gemini (new SDK)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.0-flash"

# Knowledge base for Presidency University
SYSTEM_INSTRUCTION = """You are an AI-powered Campus Helpdesk assistant for Presidency University.
Your job is to help students with queries related to campus life, academics, and services.
Only answer based on the information provided below. If the answer is not in the provided information,
clearly state that you don't have that specific information and suggest they contact the relevant department.
Do NOT make up facts, dates, or specific details that are not provided.

=== PRESIDENCY UNIVERSITY CAMPUS INFORMATION ===

ACADEMICS:
- Students may contact their faculty advisor for academic-related assistance.
- Academic concerns include course selection, syllabus queries, and subject-related guidance.
- Faculty advisors are assigned per department and can be reached through the department office.

ATTENDANCE:
- Students should follow the minimum attendance requirement prescribed by university regulations.
- Attendance records are maintained by respective faculty members.
- Students with attendance shortages should consult their faculty advisor immediately.

EXAMINATIONS:
- Examination timetables and notifications are published through official university channels.
- Students should regularly check official notice boards and the university website for exam schedules.
- For exam-related queries, contact the Examination Cell through official channels.

PLACEMENTS:
- Students may contact the Placement Department for training and placement-related information.
- The Placement Department handles internship opportunities, campus recruitment, and placement training.
- Students interested in placement activities should register with the Placement Department.

LIBRARY:
- Students may access library resources according to the library's timings and regulations.
- The library provides access to books, journals, digital resources, and study spaces.
- Library membership is available for all enrolled students.
- For library-related queries, contact the library staff during operating hours.

HOSTEL:
- Hostel-related complaints should be submitted to the Hostel Administration.
- The Hostel Administration handles room allocation, maintenance requests, and disciplinary matters.
- Students residing in hostels should follow hostel rules and regulations.

ADMINISTRATION:
- Students may contact the respective administrative office for certificates and student records.
- Administrative services include issuance of bonafide certificates, transcripts, and other official documents.
- The administrative office handles student enrollment, fee-related queries, and official documentation.

EVENTS:
- University event announcements are shared through official communication channels.
- Students should follow the university's official notice boards, website, and email for event updates.
- For event participation and organization, contact the Student Affairs Office.

=== RESPONSE GUIDELINES ===
- Be friendly, helpful, and professional.
- Keep responses concise but informative.
- If a question falls outside the provided information, say clearly that you don't have that specific detail and suggest contacting the relevant department or checking official university channels.
- Always encourage students to verify important information through official university channels.
- Address the student warmly.
- Format responses with bullet points or short paragraphs for readability.
"""


class QueryRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/chat")
async def chat(request: QueryRequest):
    try:
        user_message = request.message.strip()
        if not user_message:
            return JSONResponse({"response": "Please enter a question."}, status_code=400)

        response = client.models.generate_content(
            model=MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3,
                max_output_tokens=512,
            ),
        )

        ai_response = response.text
        return JSONResponse({"response": ai_response, "status": "success"})

    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        if "API_KEY" in error_msg.upper() or "api key" in error_msg.lower() or "INVALID_ARGUMENT" in error_msg:
            return JSONResponse(
                {"response": "⚠️ API configuration error. Please check the server configuration.", "status": "error"},
                status_code=500,
            )
        return JSONResponse(
            {"response": "⚠️ I'm experiencing technical difficulties. Please try again shortly.", "status": "error"},
            status_code=500,
        )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Campus Helpdesk AI", "model": MODEL}


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
