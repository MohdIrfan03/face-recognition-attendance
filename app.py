import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Face Recognition Attendance",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN CREDS ----------------
USERNAME = "admin"
PASSWORD = "admin123"

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #667eea, #764ba2, #43cea2, #185a9d);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(15px);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.header {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    padding: 25px;
    border-radius: 18px;
    color: white;
    font-size: 34px;
    font-weight: bold;
    text-align: center;
}

.metric {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

.footer {
    text-align: center;
    color: #eee;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; justify-content:center;">
        <div class="card" style="width:420px;">
            <h2 style="text-align:center; color:white;">🔐 Admin Login</h2>
            <p style="text-align:center; color:#eee;">
                Face Recognition Attendance System
            </p>
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
        page = st.radio("Navigate", ["Dashboard", "Attendance Records", "About"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # -------- HEADER --------
    st.markdown('<div class="header">Face Recognition Attendance Dashboard</div>', unsafe_allow_html=True)
    st.write("")

    # -------- DATE SELECTOR (CRITICAL FIX) --------
    selected_date = st.date_input(
        "📅 Select Attendance Date",
        value=date(2026, 2, 7)   # MATCH YOUR CSV DATE
    )

    formatted_date = selected_date.strftime("%d-%m-%Y")
    file_path = f"Attendance/Attendance_{formatted_date}.csv"

    st.caption(f"📄 Loading file: {file_path}")

    # -------- DEBUG (SAFE TO KEEP) --------
    if os.path.exists("Attendance"):
        st.success("✅ Attendance folder found")
    else:
        st.error("❌ Attendance folder NOT found")

    if os.path.exists(file_path):
        st.success("✅ Attendance file found")
    else:
        st.error("❌ Attendance file NOT found")

    # -------- DASHBOARD --------
    if page == "Dashboard":
        st.subheader("📊 Overview")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            col1, col2, col3 = st.columns(3)

            col1.markdown(
                f'<div class="card">👥 Total Students<br><div class="metric">{len(df)}</div></div>',
                unsafe_allow_html=True
            )
            col2.markdown(
                f'<div class="card">📚 Subjects<br><div class="metric">{df["SUBJECT"].nunique()}</div></div>',
                unsafe_allow_html=True
            )
            col3.markdown(
                f'<div class="card">📅 Date<br><div class="metric">{formatted_date}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.warning("No attendance data for selected date")

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
                file_name=f"Attendance_{formatted_date}.csv"
            )
        else:
            st.warning("No attendance found for this date")

    # -------- ABOUT --------
    else:
        st.subheader("ℹ️ About Project")
        st.markdown("""
        **Face Recognition Attendance System**

        An AI-powered attendance solution using
        computer vision and machine learning.

        **Features**
        - Face recognition using OpenCV & KNN
        - Secure admin login
        - Subject-wise attendance
        - Cloud-based dashboard

        **Tech Stack**
        Python, OpenCV, Machine Learning, Streamlit
        """)

    st.markdown('<div class="footer">© 2026 | WEB-O-THON 2.0</div>', unsafe_allow_html=True)
