import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------------- CONFIG ----------------
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

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>

/* Animated gradient background */
.stApp {
    background: linear-gradient(-45deg, #667eea, #764ba2, #43cea2, #185a9d);
    background-size: 400% 400%;
    animation: gradientBG 14s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(14px);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    animation: fadeUp 0.9s ease;
}

@keyframes fadeUp {
    from {opacity: 0; transform: translateY(30px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Header */
.header {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    padding: 28px;
    border-radius: 18px;
    color: white;
    font-size: 34px;
    font-weight: bold;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

/* Login title */
.login-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #eee;
    margin-bottom: 20px;
    font-size: 14px;
}

/* Metric text */
.metric {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #eee;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <div class="card" style="width:420px;">
            <div class="login-title">🎓 Smart Attendance</div>
            <div class="subtitle">
                Face Recognition Based Attendance System
            </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ================= MAIN APP =================
else:
    # -------- SIDEBAR --------
    with st.sidebar:
        st.title("🎓 Menu")
        page = st.radio(
            "Navigate",
            ["Dashboard", "Attendance Records", "About"]
        )
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # -------- HEADER --------
    st.markdown('<div class="header">Face Recognition Attendance Dashboard</div>', unsafe_allow_html=True)
    st.write("")

    date = datetime.now().strftime("%d-%m-%Y")
    file_path = f"Attendance/Attendance_{date}.csv"

    # -------- DASHBOARD --------
    if page == "Dashboard":
        st.subheader("📊 Overview")

        col1, col2, col3 = st.columns(3)

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            col1.markdown(
                f'<div class="card">👥 Total Students<br><div class="metric">{len(df)}</div></div>',
                unsafe_allow_html=True
            )
            col2.markdown(
                f'<div class="card">📚 Subjects<br><div class="metric">{df["SUBJECT"].nunique()}</div></div>',
                unsafe_allow_html=True
            )
            col3.markdown(
                f'<div class="card">📅 Date<br><div class="metric">{date}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.warning("No attendance data available today")

    # -------- RECORDS --------
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
                "⬇ Download CSV",
                df.to_csv(index=False),
                file_name=f"Attendance_{date}.csv"
            )
        else:
            st.warning("No attendance found")

    # -------- ABOUT --------
    else:
        st.subheader("ℹ️ About Project")
        st.markdown("""
        **Face Recognition Attendance System**

        A modern AI-powered attendance solution using
        computer vision and machine learning.

        **Key Features**
        - Face recognition using OpenCV & KNN  
        - Secure login interface  
        - Subject-wise attendance  
        - Cloud-deployed dashboard  

        **Tech Stack**
        Python, OpenCV, Machine Learning, Streamlit
        """)

    st.markdown('<div class="footer">© 2026 | WEB-O-THON 2.0</div>', unsafe_allow_html=True)
