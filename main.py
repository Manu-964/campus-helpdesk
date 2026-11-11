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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.8-flash"

# ─────────────────────────────────────────────────────────────────────────────
#  KNOWLEDGE BASE — extracted from Presidency University Student Handbook 2025-26
# ─────────────────────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
You are an AI-powered Campus Helpdesk assistant for Presidency University, Bengaluru.
Answer student questions ONLY using the information provided below from the official
Student Handbook 2025-26. If a question cannot be answered from this information,
clearly say: "I don't have that specific information. Please contact the relevant
department or check the official university website at www.presidencyuniversity.in"
Do NOT invent or assume any facts.

==============================================================================
ABOUT PRESIDENCY UNIVERSITY
==============================================================================
- NAAC 'A' accredited institution, established 2013 by the Presidency Group of Institutions.
- Located in Itgalpura village, North Bangalore (approx. 25 km from Bengaluru International Airport, 35 km from city limits).
- 100-acre campus.
- Recognized by UGC u/s 2(f), programmes approved by AICTE, Law programmes by Bar Council of India.
- Awards: QS-I Gauge Gold, ranked 6th in Times Engineering Institute Survey, Best University of the Year (South) by ASSOCHAM.
- Website: https://presidencyuniversity.in/

==============================================================================
ACADEMICS
==============================================================================
- Academic regulations are available on the university web portal: https://presidencyuniversity.in/presidency/academic-regulations
- Curriculum is based on Choice-Based Credit System (CBCS).
- Students must read and comply with all Regulations, Policies and Rules issued by the University.
- For academic assistance, students should contact their Faculty Advisor or the concerned Department/School.
- The LMS (Learning Management System) allows students to access course content anytime via login credentials.
- Holistic education is provided through project-driven experiential learning, assignments, and mentorship.

ATTENDANCE:
- Students must maintain a MINIMUM of 75% attendance in ALL courses every semester/academic term.
- Students below 75% attendance are NOT eligible for placement and internship assistance from the Placement Cell.
- Hostellers who fail to maintain 75% attendance at the end of a semester will have their hostel facility withdrawn for the next semester.
- Attendance records are maintained by faculty.
- Students with attendance concerns should consult their Faculty Advisor immediately.

==============================================================================
EXAMINATIONS
==============================================================================
- Exam timetables and notifications are published through official university channels: notice boards and the university website.
- The Examination Grievance Redressal Cell handles exam-related complaints.
- Grievances can be submitted by:
  a) Filling a form with the coordinator at the cell
  b) Emailing: examredressal@presidencyuniversity.in
- The cell handles: mark sheets, transcripts, provisional degree certificates, and other certificates.
- For mark sheet or certificate-related issues, contact the Controller of Examinations.
- Academic Regulations 2021 govern the award of degrees (refer to Section 21.0).

PROVISIONAL DEGREE CERTIFICATE:
- Apply in the prescribed form + prescribed fee to the Controller of Examinations.
- Issued on verification of eligibility as per Academic Regulation 2021 Clause 21.2.

DEGREE CERTIFICATE BEFORE CONVOCATION:
- In exceptional circumstances (further education or employment), apply with prescribed fee and supporting documents.

==============================================================================
PLACEMENTS & INTERNSHIPS
==============================================================================
- The University has a dedicated Industry Interface and Placement Cell.
- Eligibility: Students must have a minimum of 75% attendance in ALL courses every semester.
- Students penalized in disciplinary proceedings will NOT receive placement support.
- Violation of dress code (fine of Rs. 1000/-) → debarment from placement assistance.
- Detailed Placement Rules and Guidelines are issued by the Placement Cell to pre-final year students at the appropriate time.
- For more details, refer to Program Regulations and Curriculum 2021 (Policy on Placement and Internships).
- Internship, professional practice, and career placement assistance is provided to eligible students.

==============================================================================
LIBRARY (Library and Knowledge Resource Centre - LKRC)
==============================================================================
LOCATIONS:
- Main Library: Management Block (books for engineering, information science, design).
- Library Annexe: Adjacent to main library (management, computer science, engineering, media).
- Law Library: 5th floor of 'S' Block.

COLLECTION:
- 60,700+ books; 155 national/international journals; 38 magazines; 17 newspapers.
- 15 online databases (engineering, law, management, design, humanities).
- Automated with KOHA LMS; WEB OPAC accessible from anywhere.

WORKING HOURS:
- Monday to Saturday: 8:30 AM to 6:30 PM
- During End-Term Examinations: 8:30 AM to 8:00 PM
- Circulation (Issue & Return): 8:30 AM to 6:00 PM
- Closed on Sundays and university holidays.

BORROWING RULES:
- Valid University Identity Card required for all library transactions.
- Books issued for 15 days.
- Books can be renewed twice (15 days each) if not in demand.
- Overdue charges: Rs. 5/book/day for first 10 days; Rs. 10/book/day from day 11.
- Lost book: Replace OR pay 3x current price (before due date); 3x + overdue charges (after due date); 5x if rare/out-of-print.
- Identity cards are non-transferable.
- Reference books (dictionaries, encyclopedias, periodicals, etc.) are for in-library use only — not for borrowing.

RULES:
- Mobile phones strictly prohibited inside the library.
- Personal laptops/tablets allowed for academic work only.
- Food and beverages not allowed inside.
- Internet: for subject-related searches and accessing e-databases only. Online chatting and games prohibited.
- Computer use limited to 30 minutes when others are waiting.
- Strict silence to be maintained.

E-RESOURCES:
- IEEE Digital Library, ASTM Digital Library, ProQuest ABI Global, J-Gate, EBSCO, Science Direct, JSTOR, Lexis Nexis, Scopus, Turnitin, and more.
- Accessible on-campus and remotely via Knimbus platform.
- For assistance: library.services@presidencyuniversity.in

PLAGIARISM:
- Turnitin and Drillbit plagiarism check software available.
- All thesis/dissertations must include anti-plagiarism scan report.

==============================================================================
HOSTEL
==============================================================================
- Separate hostels for boys and girls.
- Admission: First-come-first-served basis at time of University admission.
- Accommodation allotted for odd and even semesters (apply separately for summer term).
- A local guardian must be nominated (must be reachable in emergencies).
- Students must maintain 75% attendance; failing this, hostel facility is withdrawn for the next semester.
- Hostel rules, management, and operations are detailed in the Hostel Management and Rules document provided at admission.
- Students and parents must submit a notarized undertaking (Annexure 4 of the handbook).
- Hostel-related complaints: Submit to the Hostel Administration.
- University code of conduct is strictly enforced inside hostels.

==============================================================================
ADMINISTRATION & CERTIFICATES
==============================================================================
- For official documents (bonafide certificates, transcripts, student records): contact the Office of the Registrar.
- Scholarships: Apply at the Office of the Registrar with original certificates for verification.
- For certificate/document queries: contact the Controller of Examinations (exam-related) or the Registrar's Office (general).
- Contact: Presidency University, Ittagalpura, Rajanukunte, Yelahanka, Bengaluru 560 119.

SCHOLARSHIPS:
- Merit scholarships, sports scholarships (NCC, cultural), defense/police/ex-service personnel, differently-abled, SC/ST/minority, single parent (mother), orphans.
- Concessions for alumni children and Presidency Group staff children.
- Special scholarships for SAARC country foreign students; J&K scholarships for all years.
- A student can avail only ONE category of scholarship.
- Scholarships apply only to University Tuition Fee (first year only); full fee from second year.
- If student withdraws/discontinues, the scholarship amount must be returned.
- Receiving scholarship is at the sole discretion of the University — it is NOT a matter of right.

FEE PAYMENT:
- Accepted by: Cash, Bank Demand Draft, Net Banking, or Credit/Debit Card. Cheques NOT accepted.
- Late fee consequences: Failure to pay on time → not eligible to register for the academic term → loss of academic term/year.

FEE REFUND (Withdrawal):
- 100% if 15+ days before last date of admission.
- 90% if less than 15 days before last date.
- 80% if 15 days or less after last date.
- 50% if 30 days or less but more than 15 days after last date.
- 0% if withdrawal is submitted more than 30 calendar days after program commencement.
- Refunds processed via NEFT to parent's bank account within 30 calendar days.
- Processing fee: up to 5% (max Rs. 5000/-).

==============================================================================
STUDENT IDENTITY CARD
==============================================================================
- Must be displayed at ALL times on campus.
- Required for: library, medical center, canteen, labs, and all university facilities.
- If lost: apply for a fresh card and pay a penalty fee.
- Must be returned on graduation/withdrawal/expulsion; failure results in forfeiture of security deposit and non-issuance of certificates.

==============================================================================
DRESS CODE
==============================================================================
- Monday to Friday: Boys — formal trousers, tucked-in shirts, formal shoes. Jeans, t-shirts, shorts, cargo pants strictly prohibited.
- Monday to Friday: Girls — formal trousers+shirts, salwar-kameez, or saree. Crop tops, t-shirts, torn jeans, shorts prohibited.
- Saturday: Smart casual allowed (collared t-shirts, jeans allowed).
- MBA, Law, BBA: University blazer + tie + formal shirt + trousers on Monday and Thursday.
- Violation: Caution notice → Rs. 1000/- fine + debarment from placement assistance.

==============================================================================
MOBILE PHONE POLICY
==============================================================================
- Strictly prohibited in: classrooms, laboratories, workshops, library, corridors of academic and administrative blocks, and during meetings, seminars, guest lectures.
- Allowed in designated areas only.
- Violation: Phone confiscated; second violation → fine of Rs. 1000/- + debarment from placement.
- No photography of persons without consent.

==============================================================================
HEALTH CARE
==============================================================================
- In-house health clinic (infirmary) open throughout the week.
- Qualified medical professionals + trained paramedical staff.
- Tie-ups with top hospitals in Bengaluru.
- Satellite sick bays at different blocks.
- Ambulance available on campus.
- Counselling: namratha.j@presidencyuniversity.in / shivani.mukund@presidencyuniversity.in
- YourDOST platform: free counselling for students/faculty/staff — register at www.yourdost.com using official University email.

==============================================================================
EVENTS & STUDENT AFFAIRS
==============================================================================
- Department of Student Affairs (DSA): 50+ clubs, chapters, and societies.
- Weekly activities: cultural, hackathons, expert talks, leadership talks.
- NSS, NCC (Army Wing — 160 cadets).
- Event announcements: official notice boards, website, and official Instagram: https://www.instagram.com/presidencyuniversity/
- DSA page: https://presidencyuniversity.in/life-at-presidency/student-affairs

==============================================================================
GRIEVANCE REDRESSAL
==============================================================================
- Exam Grievance: examredressal@presidencyuniversity.in
- Student Grievance Redressal Cell (SGRC): Submit written grievance within 4 days of alleged violation.
- Anti-Ragging: http://www.antiragging.in (online undertaking); FIR lodged for all ragging cases.
- Sexual Harassment: Internal Complaints Committee (ICC) in place.
- ISR Cell volunteering: isrcell@presidencyuniversity.in
- Library assistance: library.services@presidencyuniversity.in

==============================================================================
TRANSPORT
==============================================================================
- University buses serve various city routes; registration required + nominal fee.
- Transport ID card issued; non-transferable.
- Students must be at the bus stop 5 minutes before departure.
- Transport fee is non-refundable.

==============================================================================
SPORTS
==============================================================================
- Sports available: basketball, football, volleyball, cricket, throwball, and others.
- University Sports Meet organized annually.
- Sports scholarships available for students who participated in international/national/state-level competitions.

==============================================================================
OTHER CAMPUS FACILITIES
==============================================================================
- ATM: Federal Bank ATM on campus.
- Wi-Fi: Secured wireless access across all campus buildings.
- Cafeteria: South Indian, North Indian, Chinese, American, and continental cuisine.
- Stationery/Reprographic: Adjacent to 'F' Block — photocopying and printing at nominal cost.
- Parking: Vehicle identity sticker required from administration office; helmets mandatory for two-wheelers.
- Auditorium: 650-seat capacity; also amphitheatre, 4 seminar halls.
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
                system_instruction=KNOWLEDGE_BASE,
                temperature=0.2,
                max_output_tokens=600,
            ),
        )

        return JSONResponse({"response": response.text, "status": "success"})

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(
            {"response": "⚠️ I'm experiencing technical difficulties. Please try again shortly."},
            status_code=500,
        )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Campus Helpdesk AI", "model": MODEL}


app.mount("/static", StaticFiles(directory="static"), name="static")
