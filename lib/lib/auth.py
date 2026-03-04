import streamlit as st
from lib.supabase_client import get_supabase, creator_email

def login_ui():
    sb = get_supabase()

    mode = st.sidebar.radio("Mode", ["Login","Sign up"])

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if mode == "Sign up":
        if st.sidebar.button("Create account"):
            sb.auth.sign_up({"email": email, "password": password})
            st.sidebar.success("Account created")

    if mode == "Login":
        if st.sidebar.button("Log in"):
            res = sb.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state["sb_user"] = res.user.model_dump()

def logout_ui():
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

def ensure_profile():
    pass

def get_my_role():
    user = st.session_state.get("sb_user")
    if not user:
        return "anonymous"
    if user.get("email","").lower() == creator_email():
        return "creator"
    return "athlete"
