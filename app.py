import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Face Recognition Attendance",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- CREDENTIALS ----------------
USERNAME = "admin"
PASSWORD = "admin123"

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>

/* Animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #667eea, #764ba2, #ff758c, #ff7eb3);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass card */
.card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    animation: slideFade 1.2s ease;
}

@keyframes slideFade {
    from {opacity: 0; transform: translateY(40px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Header */
.header {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    padding: 25px;
    border-radius: 15px;
    color: white;
    font-size: 34px;
    font-weight: bold;
    text-align: center;
}

/* Title glow */
.title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #fff; }
    to { text-shadow: 0 0 20px #ffdee9; }
}

.subtitle {
    text-align: center;
    color: #eee;
    font-size: 14px;
    margin-bottom: 25px;
}

.footer {
    text-align: center;
    color: #eee;
    margin-top: 40px;
    font-size: 14px;
}

.metric {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ================= LOGIN PAGE =================
if not st.session_state.logged_in:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <div class="card" style="width:400px;">
            <div class="title">🎓 Smart Attendance</div>
            <div class="subtitle">
                Face Recognition Based Attendance System
            </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ================= MAIN DASHBOARD =================
else:
    # -------- SIDEBAR --------
    with st.sidebar:
        st.title("🎓 Navigation")
        page = st.radio(
            "Go to",
            ["Dashboard", "Attendance Records", "About Project"]
        )
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # -------- HEADER --------
    st.markdown('<div class="header">Face Recognition Attendance Dashboard</div>', unsafe_allow_html=True)
    st.write("")

    # -------- DATE SELECTOR --------
    selected_date = st.date_input("📅 Select Attendance Date", datetime.today())
    date = selected_date.strftime("%d-%m-%Y")
    file_path = f"Attendance/Attendance_{date}.csv"

    # -------- DASHBOARD PAGE --------
    if page == "Dashboard":
        st.subheader("📊 Overview")

        col1, col2, col3 = st.columns(3)

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            col1.markdown(f'<div class="card">👥 Total Students<br><div class="metric">{len(df)}</div></div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="card">📚 Subjects<br><div class="metric">{df["SUBJECT"].nunique()}</div></div>', unsafe_allow_html=True)
            col3.markdown(f'<div class="card">📅 Date<br><div class="metric">{date}</div></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠ No attendance data available for selected date")

    # -------- RECORDS PAGE --------
    elif page == "Attendance Records":
        st.subheader("📁 Attendance Records")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            subject = st.selectbox(
                "Filter by Subject",
                ["All"] + list(df["SUBJECT"].unique())
            )

            if subject != "All":
                df = df[df["SUBJECT"] == subject]

            st.dataframe(df, use_container_width=True)

            st.download_button(
                "⬇ Download Attendance CSV",
                df.to_csv(index=False),
                file_name=f"Attendance_{date}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠ No attendance found for selected date")

    # -------- ABOUT PAGE --------
    else:
        st.subheader("ℹ️ About Project")
        st.markdown("""
        **Face Recognition Attendance System**

        An AI-powered system that automates attendance using
        computer vision and machine learning.

        **Features**
        - Face recognition using OpenCV & KNN
        - Secure login system
        - Subject-wise attendance
        - Duplicate prevention
        - Cloud-based dashboard

        **Tech Stack**
        Python, OpenCV, Machine Learning, Streamlit
        """)

    st.markdown('<div class="footer">© 2026 | WEB-O-THON 2.0 | Team Project</div>', unsafe_allow_html=True)
