import streamlit as st
import hashlib

# Set up page configuration
st.set_page_config(page_title="AQI Dashboard", page_icon="🌍")

# Dummy user data (for demonstration purposes only, replace with a secure system in production)
users = {
    "user1": {"password": hashlib.sha256("password1".encode()).hexdigest(), "is_first_time": True},
    "user2": {"password": hashlib.sha256("password2".encode()).hexdigest(), "is_first_time": False},
}

# User Authentication
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    if username in users:
        if users[username]["password"] == hash_password(password):
            return True, users[username]["is_first_time"]
    return False, False

def sign_up(username, password):
    users[username] = {"password": hash_password(password), "is_first_time": True}
    return True

# Chatbot function (simple demo)
def chatbot_response(user_input):
    responses = {
        "hello": "Hi there! How can I assist you with the AQI dashboard?",
        "how to use": "You can explore the AQI data in the dashboard below. Select a location or use filters to customize the view.",
        "what is aqi": "AQI stands for Air Quality Index. It indicates how clean or polluted the air is in a specific area.",
    }
    return responses.get(user_input.lower(), "I'm here to help! Try asking about AQI or how to use the dashboard.")

# App layout
st.title("🌍 AQI Dashboard")

# Login/Sign-Up Section
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.sidebar.title("Welcome!")
    st.sidebar.write("Please log in or sign up to access the AQI Dashboard.")

    option = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if option == "Login":
        if st.sidebar.button("Log In"):
            success, is_first_time = login(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["is_first_time"] = is_first_time
                st.sidebar.success("Logged in successfully!")
            else:
                st.sidebar.error("Invalid credentials.")
    elif option == "Sign Up":
        if st.sidebar.button("Sign Up"):
            if username in users:
                st.sidebar.error("Username already exists. Try logging in.")
            else:
                sign_up(username, password)
                st.sidebar.success("Signed up successfully! Please log in.")
else:
    # Welcome message for first-time users
    if st.session_state["is_first_time"]:
        st.success("Welcome to the AQI Dashboard! Here are some tips to get started...")
        st.write("""
        - Use the embedded Power BI dashboard below to view AQI data.
        - Try the interactive filters and controls to customize your view.
        """)

    # Display AQI Dashboard iframe
    st.write("Explore the AQI Dashboard below:")
    st.markdown("""
    <iframe title="AQI Finaldashboard aman" width="100%" height="500" 
    src="https://app.powerbi.com/view?r=eyJrIjoiNWJmZmJmOTYtMjEzNi00YmRiLTgwMWUtYzcxZjI3YzdmNDVhIiwidCI6IjY2NmM0YmJlLTViY2YtNDU5ZS1hN2M5LTdmYjM3NjgxNzYzNiJ9" 
    frameborder="0" allowFullScreen="true"></iframe>
    """, unsafe_allow_html=True)

    # Interactive location filter
    location = st.selectbox("Select a Location", ["Location 1", "Location 2", "Location 3"])
    st.write(f"You selected: {location}")

    # Chatbot interaction
    st.write("💬 Chatbot")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_input = st.text_input("Ask something about AQI or the dashboard:", key="chatbot_input")
    if st.button("Send"):
        response = chatbot_response(user_input)
        st.session_state["chat_history"].append({"user": user_input, "bot": response})

    for chat in st.session_state["chat_history"]:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")

    # Log out button
    if st.sidebar.button("Log Out"):
        st.session_state["logged_in"] = False
        st.session_state["chat_history"] = []
        st.session_state["is_first_time"] = False
        st.experimental_rerun()
