# voting_system.py
import streamlit as st
import base64
from datetime import datetime

def add_tailwind():
    tailwind_cdn = """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
    """
    st.markdown(tailwind_cdn, unsafe_allow_html=True)

def voter_registration():
    st.header("📝 Voter Registration")
    with st.form("registration_form"):
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        voter_id = st.text_input("Voter ID")
        uploaded_photo = st.file_uploader("Upload Your Photo", type=['jpg', 'png'])
        submitted = st.form_submit_button("Register")
        if submitted:
            st.success(f"Voter {name} registered successfully!")
            # Save details logic here

def facial_data_capture():
    st.header("📷 Facial Data Capture")
    uploaded_face = st.file_uploader("Capture/Upload Facial Image", type=['jpg', 'png'])
    if uploaded_face:
        st.image(uploaded_face, caption="Captured Face", use_column_width=True)
        st.success("Facial data captured and stored securely.")


def voting_interface():
    st.header("🗳️ Voting Interface")
    candidate = st.radio("Choose your candidate:", ("Candidate A", "Candidate B", "Candidate C"))
    if st.button("Cast Vote"):
        st.success(f"Your vote for {candidate} has been cast successfully!")


def vote_confirmation():
    st.header("✅ Vote Confirmation")
    st.info("Your vote has been recorded. Thank you for voting!")


def result_announcement():
    st.header("📢 Result Announcement")
    st.info("Results will be displayed here after voting closes.")

add_tailwind()
st.sidebar.title("📋 Voting System")
section = st.sidebar.selectbox("Choose a section:", (
    "Voter Registration",
    "Facial Data Capture",
    "Voting Interface",
    "Vote Confirmation",
    "Result Announcement"
))

if section == "Voter Registration":
    voter_registration()
elif section == "Facial Data Capture":
    facial_data_capture()
elif section == "Voting Interface":
    voting_interface()
elif section == "Vote Confirmation":
    vote_confirmation()
elif section == "Result Announcement":
    result_announcement()
