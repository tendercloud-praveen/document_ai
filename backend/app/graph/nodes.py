import json
from pathlib import Path

from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os
from langchain_core.messages import HumanMessage

from app.graph.state import DocumentState

from PIL import Image
from datetime import datetime
import pytesseract

load_dotenv()


# =========================
# 🔥 TESSERACT PATH (IMPORTANT)
# =========================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# =========================
# LLM
# =========================
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     temperature=0,
# )
llm = ChatGroq(
    model="llama-3.3-70b-versatile",   # or another Groq-supported model
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


# =========================
# UPLOAD NODE
# =========================
def upload_node(state: DocumentState):
    print("Uploaded File:", state["file_path"])
    return state


# =========================
# OCR NODE (FIXED + SAFE)
# =========================
def ocr_node(state: DocumentState):
    print("OCR Node")

    file_path = Path(state["file_path"])

    try:
        image = Image.open(file_path)
        image = image.convert("RGB")
        raw_text = pytesseract.image_to_string(image)

    except Exception as e:
        print("OCR ERROR:", e)
        raw_text = ""

    state["raw_text"] = raw_text

    print("OCR extracted length:", len(raw_text))
    print("RAW TEXT:")
    print(raw_text)

    return state
    
# =========================
# LLM NODE (FIXED JSON SAFE)
# =========================
def llm_node(state: DocumentState):
    print("LLM Node")

    raw_text = state.get("raw_text", "")

    prompt = f"""
You are an Intelligent Document Processing (IDP) AI.

OCR TEXT:
----------------
{raw_text}
----------------

Identify the document type.

Supported document types:
- Invoice
- Resume
- Aadhaar Card
- PAN Card
- Passport
- Driving License
- Receipt
- Purchase Order
- Bank Statement
- Payslip
- Offer Letter
- Contract
- Medical Record
- Insurance Claim
- Unknown

Extract only the relevant fields.

Invoice:
invoice_number
invoice_date
vendor_name
customer_name
total_amount
tax
currency

Resume:
name
email
phone
skills
education
experience

PAN Card:
pan_number
name
father_name
date_of_birth

Aadhaar Card:
aadhaar_number
name
date_of_birth
gender
address

Passport:
passport_number
name
nationality
date_of_birth
expiry_date

Driving License:
license_number
name
date_of_birth
issue_date
expiry_date

Receipt:
receipt_number
merchant_name
date
total_amount

Purchase Order:
po_number
vendor_name
order_date
total_amount

Bank Statement:
account_holder
account_number
bank_name
opening_balance
closing_balance

Payslip:
employee_name
company_name
pay_period
net_salary

Offer Letter:
employee_name
company_name
designation
joining_date
salary

Contract:
party_1
party_2
effective_date
termination_date

Medical Record:
patient_name
doctor_name
hospital
diagnosis

Insurance Claim:
claim_number
policy_number
claimant_name
claim_amount

If the document type is unknown, return an empty fields object.

Return ONLY valid JSON in this format:

{{
    "document_type":"",
    "confidence":0,
    "summary":"",
    "fields":{{}}
}}

Rules:
- Never invent values.
- Missing values should be "".
- Return only JSON.
- No markdown.
- No explanation.
"""

    message = HumanMessage(content=prompt)

    try:
        print(prompt)
        response = llm.invoke([message])

        print("RAW RESPONSE:")

        print(response.content)

        content = response.content.strip()

        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        data = json.loads(content)

    except Exception as e: 
        print("LLM ERROR:", e)

        data = {
            "document_type": "Unknown",
            "confidence": 0,
            "summary": "",
            "fields": {}
        }
    

    # state["document_type"] = data.get("document_type", "Unknown")
    # state["confidence"] = data.get("confidence", 0)
    # state["summary"] = data.get("summary", "")
    # state["extracted_data"] = data.get("fields", {})

    # print("FINAL RESULT")
    # print(json.dumps(data, indent=4))

    # return state
    state["document_type"] = data.get("document_type", "Unknown")
    state["confidence"] = data.get("confidence", 0)
    state["summary"] = data.get("summary", "")
    state["extracted_data"] = data.get("fields", {})
    confidence = float(state["confidence"])
    if confidence >= 0.90:
        state["status"] = "Approved"
        state["approved_by"] = "System"
        state["approved_date"] = datetime.now()
    else:
        state["status"] = "Pending" 
        state["approved_by"] = None
        state["approved_date"] = None
    print("FINAL RESULT")
    print(json.dumps(data, indent=4))
    return state

    

    
