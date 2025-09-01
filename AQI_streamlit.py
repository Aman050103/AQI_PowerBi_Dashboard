import streamlit as st
import base64
import pandas as pd
import plotly.express as px

# ----------------- CONFIG -----------------
st.set_page_config(page_title="📊 Air Quality Dashboard", layout="wide")

# Dummy credentials
ADMIN_USERNAME = "aman"
ADMIN_PASSWORD = "0888"

# ----------------- SESSION STATE -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "show_admin_form" not in st.session_state:
    st.session_state.show_admin_form = False

# ----------------- BACKGROUND IMAGE -----------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64_of_bin_file("background.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

.login-box {{
    background: rgba(255, 255, 255, 0.85);
    padding: 40px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    width: 380px;
    margin: auto;
}}
.stButton>button {{
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 16px;
    font-weight: bold;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------- LOGIN PAGE -----------------
def login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)  # spacing
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("## 📊 Air Quality Dashboard")

        if not st.session_state.show_admin_form:
            st.write("### Choose Login Mode")

            if st.button("👑 Login as Admin"):
                st.session_state.show_admin_form = True

            st.write("OR")

            if st.button("🙋 Login as Guest"):
                st.session_state.logged_in = True
                st.session_state.role = "guest"
                st.rerun()

        # --- Admin Login Form ---
        if st.session_state.show_admin_form and not st.session_state.logged_in:
            st.write("### 👑 Admin Login")

            username = st.text_input("👤 Username", key="admin_user")
            password = st.text_input("🔑 Password", type="password", key="admin_pass")

            if st.button("✅ Login"):
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.show_admin_form = False
                    st.success("✅ Login successful! Welcome Admin.")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

            if st.button("⬅️ Back"):
                st.session_state.show_admin_form = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- MAIN APP -----------------
def main_app():
    st.title("📊 Air Quality Dashboard")
    st.markdown(f"### You are logged in as: **{st.session_state.role.capitalize()}**")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.show_admin_form = False
        st.rerun()

    if st.session_state.role == "admin":
        st.subheader("🔑 Admin Access")
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiYWJlN2RmYzctOTRjOS00NmI1LWI4N2ItNzFkYWU2ZmQwMDQ3IiwidCI6IjM0YmQ4YmVkLTJhYzEtNDFhZS05ZjA4LTRlMGEzZjExNzA2YyJ9"
        st.components.v1.iframe(powerbi_url, width=1000, height=600)

    elif st.session_state.role == "guest":
        st.subheader("👤 Guest Access")
        st.info("ℹ️ Limited access – You can only view sample data.")
        df = pd.DataFrame({
            "City": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
            "AQI": [180, 150, 120, 130]
        })
        fig = px.bar(df, x="City", y="AQI", title="Sample AQI Data (Guest View)")
        st.plotly_chart(fig)

# ----------------- RUN APP -----------------
if st.session_state.logged_in:
    main_app()
else:
    login()
