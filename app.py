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

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- CREDENTIALS ----------------
USERNAME = "admin"
PASSWORD = "admin123"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.login-card {
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
    width: 400px;
    margin: auto;
    margin-top: 120px;
}
.title {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
.footer {
    text-align: center;
    color: gray;
    font-size: 14px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN PAGE =================
if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-card">
        <h2 style="text-align:center;">🔐 Login</h2>
        <p style="text-align:center; color:gray;">
        Face Recognition Attendance System
        </p>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        login_btn = st.button("Login", use_container_width=True)

    if login_btn:
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")

# ================= MAIN DASHBOARD =================
else:
    st.markdown('<div class="title">🎓 Face Recognition Attendance Dashboard</div>', unsafe_allow_html=True)
    st.write("")

    # Logout button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    date = datetime.now().strftime("%d-%m-%Y")
    file_path = f"Attendance/Attendance_{date}.csv"

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(f"📅 Attendance — {date}")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            subject = st.selectbox(
                "📘 Filter by Subject",
                ["All"] + list(df["SUBJECT"].unique())
            )

            if subject != "All":
                df = df[df["SUBJECT"] == subject]

            st.dataframe(df, use_container_width=True)

            st.download_button(
                "⬇ Download CSV",
                data=df.to_csv(index=False),
                file_name=f"Attendance_{date}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠ No attendance recorded today")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Summary")

        if os.path.exists(file_path):
            st.metric("👥 Total Students", len(df))
            st.metric("📚 Subjects", df["SUBJECT"].nunique())
        else:
            st.metric("👥 Total Students", 0)
            st.metric("📚 Subjects", 0)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">© 2026 | Face Recognition Attendance System</div>',
        unsafe_allow_html=True
    )
