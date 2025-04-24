import streamlit as st
import os
import json
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
from datetime import datetime
from collections import Counter

# ------------------------
# 🌐 Tailwind CSS Styling
# ------------------------
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

# ------------------------
# 💾 Save JSON data
# ------------------------
def save_data(data, filename):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing = json.load(file)
        else:
            existing = []
        existing.append(data)
        with open(filename, "w") as file:
            json.dump(existing, file, indent=4)
    except Exception as e:
        st.error(f"Error saving data to {filename}: {e}")

# ------------------------
# 🧠 Face Detection (Mediapipe)
# ------------------------
def detect_face_mediapipe(image_file):
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    image = Image.open(image_file).convert('RGB')
    img_np = np.array(image)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(img_np)

        if results.detections:
            return True
        else:
            return False

# ------------------------
# 📝 Voter Registration
# ------------------------
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
                if os.path.exists("voters.json"):
                    with open("voters.json", "r") as file:
                        voters = json.load(file)
                    if any(v['voter_id'] == voter_id for v in voters):
                        st.error("This Voter ID is already registered.")
                        return

                # Face detection
                if not detect_face_mediapipe(uploaded_photo):
                    st.error("No face detected. Please upload a clear image with your face visible.")
                    return

                # Save image
                os.makedirs("faces", exist_ok=True)
                with open(os.path.join("faces", uploaded_photo.name), "wb") as f:
                    f.write(uploaded_photo.getbuffer())

                data = {
                    "name": name,
                    "dob": str(dob),
                    "voter_id": voter_id,
                    "photo": uploaded_photo.name,
                    "registered_at": datetime.now().isoformat()
                }
                save_data(data, "voters.json")
                st.markdown("""<div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">✅ Voter registered successfully!</div>""", unsafe_allow_html=True)
            else:
                st.error("Please fill all fields and upload a photo.")

# ------------------------
# 📸 Facial Data Capture
# ------------------------
def facial_data_capture():
    st.header("📷 Facial Data Capture")
    uploaded_face = st.file_uploader("Capture/Upload Facial Image", type=['jpg', 'png'])
    if uploaded_face:
        if detect_face_mediapipe(uploaded_face):
            os.makedirs("faces", exist_ok=True)
            with open(os.path.join("faces", uploaded_face.name), "wb") as f:
                f.write(uploaded_face.getbuffer())
            st.image(uploaded_face, caption="Captured Face", use_column_width=True)
            st.success("Facial data captured and stored securely.")
        else:
            st.error("No face detected. Please upload a clear image.")

# ------------------------
# 🗳️ Voting Interface
# ------------------------
def voting_interface():
    st.header("🗳️ Voting Interface")
    voter_id = st.text_input("Enter Your Voter ID to Vote")
    if voter_id:
        if os.path.exists("voted.json"):
            with open("voted.json", "r") as f:
                voted_list = json.load(f)
        else:
            voted_list = []

        if voter_id in voted_list:
            st.warning("You have already voted.")
            return

        candidate = st.radio("Choose your candidate:", ("Candidate A", "Candidate B", "Candidate C"))
        if st.button("Cast Vote"):
            save_data(candidate, "votes.json")
            voted_list.append(voter_id)
            with open("voted.json", "w") as f:
                json.dump(voted_list, f)
            st.markdown("""<div class="p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">✅ Your vote has been successfully submitted.</div>""", unsafe_allow_html=True)

# ------------------------
# ✅ Vote Confirmation
# ------------------------
def vote_confirmation():
    st.header("✅ Vote Confirmation")
    st.info("Your vote has been recorded. Thank you for voting!")

# ------------------------
# 📢 Result Announcement
# ------------------------
def result_announcement():
    st.header("📢 Result Announcement")
    if os.path.exists("votes.json"):
        with open("votes.json", "r") as file:
            votes = json.load(file)
        results = Counter(votes)
        st.bar_chart(results)
        st.success("Live vote count displayed.")
    else:
        st.info("No votes have been cast yet.")

# ------------------------
# ▶️ Main App Runner
# ------------------------
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
