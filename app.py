import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="VisionCV AI",
    layout="wide"
)

# ---------------- PROJECTS ----------------

projects = [
    "AI Resume System",
    "Gesture Controlled Interface",
    "Computer Vision Dashboard",
    "Real-Time Face Detection"
]

# ---------------- STYLING ----------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: black;
        color: white;
    }

    .title {
        text-align: center;
        font-size: 70px;
        font-weight: bold;
        color: cyan;
    }

    .card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid cyan;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TITLE ----------------

st.markdown(
    '<div class="title">VisionCV AI</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- READ GESTURE ----------------

gesture = "No Hand"

try:
    with open("gesture.txt", "r") as file:
        gesture = file.read()

except:
    pass

# ---------------- PROJECT SWITCH ----------------

project = projects[0]

if gesture == "Pointing":
    project = projects[1]

elif gesture == "Thumbs Up":
    project = projects[2]

elif gesture == "Open Hand":
    project = projects[3]

# ---------------- UI ----------------

col1, col2 = st.columns([1, 1])

with col1:

    st.markdown(
        f'''
        <div class="card">
            <h2>Live Gesture</h2>
            <h1 style="color:cyan;">{gesture}</h1>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f'''
        <div class="card">
            <h2>Current Project</h2>
            <h1>{project}</h1>
        </div>
        ''',
        unsafe_allow_html=True
    )

# ---------------- AUTO REFRESH ----------------

time.sleep(0.5)

st.rerun()