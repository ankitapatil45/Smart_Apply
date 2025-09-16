from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import re
import csv
from PIL import Image
import pdf2image
import PyPDF2
import google.generativeai as genai
import pandas as pd
import pickle

# ---- Config ----
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

PICKLE_FILE = "candidate_tracker.pkl"
CSV_FILE = "shortlisted_candidates.csv"

# ---- Helper Functions ----
def get_gemini_response(job_desc, pdf_content, prompt):
    """Send job description + resume to Gemini for evaluation."""
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content([job_desc, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """Convert PDF first page into base64 image for Gemini Vision."""
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def extract_text_from_pdf(uploaded_file):
    """Extract raw text from PDF file using PyPDF2."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_contact_info_from_text(text):
    """Extract email and phone number from PDF text."""
    email = None
    phone = None

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group(0)

    phone_match = re.search(r'(\+?\d{1,3}[\s-]?)?\d{10}', text)
    if phone_match:
        phone = phone_match.group(0)

    return email, phone

def save_progress(data):
    """Save candidate progress to pickle file."""
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(data, f)

def load_progress():
    """Load candidate progress from pickle file."""
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return pd.DataFrame(columns=["Candidate", "ATS Match", "Status", "Evaluation", "Email", "Phone"])

def save_shortlisted_to_csv(candidate_name, ats_match, evaluation, email, phone):
    """Save shortlisted candidate details into CSV."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Candidate", "ATS Match", "Email", "Phone", "Evaluation"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "Candidate": candidate_name,
            "ATS Match": ats_match,
            "Email": email if email else "N/A",
            "Phone": phone if phone else "N/A",
            "Evaluation": evaluation[:200]  # only store first 200 chars
        })

# ---- Streamlit App ----
st.set_page_config(page_title="Smart Apply System")
st.header("Smart Apply System – ATS Resume Screening")

# Load previous tracker
progress_data = load_progress()

# Job Description Input
job_description = st.text_area("Enter Job Description:", key="jobdesc")

# Multiple Resume Upload
uploaded_files = st.file_uploader("Upload Resumes (PDF)...", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    st.success(f"{len(uploaded_files)} resumes uploaded successfully!")

# Prompts
match_prompt = """
You are an ATS scanner. 
Evaluate the resume against the job description. 
Give a percentage match, list missing keywords, and provide final thoughts. 
Respond in structured format.
"""

# Run Screening
if st.button("Run Screening"):
    if job_description and uploaded_files:
        new_results = []
        for file in uploaded_files:
            # Convert for Gemini
            pdf_content = input_pdf_setup(file)

            # Reset pointer to read again for text extraction
            file.seek(0)
            resume_text = extract_text_from_pdf(file)

            # Get ATS evaluation from Gemini
            ats_result = get_gemini_response(job_description, pdf_content, match_prompt)

            # Extract % match
            percentage = 0
            if "%" in ats_result:
                try:
                    percentage = int(''.join(filter(str.isdigit, ats_result.split('%')[0])))
                except:
                    percentage = 0

            status = "Rejected"
            if percentage >= 60:   # shortlist threshold
                status = "Shortlisted"

            # Extract email & phone from actual resume text
            email, phone = extract_contact_info_from_text(resume_text)

            # Save shortlisted candidate to CSV
            if status == "Shortlisted":
                save_shortlisted_to_csv(file.name, f"{percentage}%", ats_result, email, phone)

            new_results.append({
                "Candidate": file.name,
                "ATS Match": f"{percentage}%",
                "Status": status,
                "Evaluation": ats_result,
                "Email": email,
                "Phone": phone
            })

        # Append new results to existing tracker
        new_df = pd.DataFrame(new_results)
        progress_data = pd.concat([progress_data, new_df], ignore_index=True)

        # Save updated tracker
        save_progress(progress_data)

        # Show progress tracker
        st.subheader("Candidate Progress Tracker")
        st.dataframe(progress_data)

        # Show shortlisted candidates
        shortlisted = progress_data[progress_data["Status"] == "Shortlisted"]
        if not shortlisted.empty:
            st.subheader("Shortlisted Candidates")
            st.write(shortlisted[["Candidate", "ATS Match", "Email", "Phone"]])
        else:
            st.info("No candidates shortlisted.")
    else:
        st.warning("Please upload resumes and enter a job description.")

# Show saved tracker anytime
if st.checkbox("Show Saved Tracker Data"):
    st.dataframe(progress_data)

    # Add delete/reset option
    if st.button("Delete Saved Tracker Data"):
        if os.path.exists(PICKLE_FILE):
            os.remove(PICKLE_FILE)  # delete pickle file
        progress_data = pd.DataFrame(columns=["Candidate", "ATS Match", "Status", "Evaluation", "Email", "Phone"])
        st.success("✅ Saved tracker data deleted successfully!")

