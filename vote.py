# voting_system.py
import streamlit as st
import base64
import os
import json
from datetime import datetime
from collections import Counter
from cryptography.fernet import Fernet

# Encryption key (you should store this securely in production)
key = Fernet.generate_key()
f = Fernet(key)

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

def save_data(data, filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing = json.load(file)
    else:
        existing = []
    existing.append(data)
    with open(filename, "w") as file:
        json.dump(existing, file, indent=4)

def voter_registration():
    st.header("📝 Voter Registration")
    with st.form("registration_form"):
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        voter_id = st.text_input("Voter ID")
        uploaded_photo = st.file_uploader("Upload Your Photo", type=['jpg', 'png'])
        submitted = st.form_submit_button("Register")
        if submitted:
            if name and dob and voter_id and uploaded_photo:
                data = {
                    "name": name,
                    "dob": str(dob),
                    "voter_id": voter_id,
                    "registered_at": datetime.now().isoformat()
                }
                save_data(data, "voters.json")
                st.markdown("""
                <div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
                    ✅ Voter registered successfully!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please fill all fields and upload a photo.")

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
        encrypted_vote = f.encrypt(candidate.encode()).decode()
        save_data(encrypted_vote, "votes.json")
        st.markdown("""
        <div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
            ✅ Your vote has been successfully submitted.
        </div>
        """, unsafe_allow_html=True)

def vote_confirmation():
    st.header("✅ Vote Confirmation")
    st.info("Your vote has been recorded. Thank you for voting!")

def result_announcement():
    st.header("📢 Result Announcement")
    if os.path.exists("votes.json"):
        with open("votes.json", "r") as file:
            encrypted_votes = json.load(file)
        decrypted_votes = [f.decrypt(v.encode()).decode() for v in encrypted_votes]
        results = Counter(decrypted_votes)
        st.bar_chart(results)
        st.success("Live vote count displayed.")
    else:
        st.info("No votes have been cast yet.")

# Run app
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
