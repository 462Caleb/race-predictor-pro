import streamlit as st
from lib.supabase_client import get_supabase, creator_email

def login_ui():
    sb = get_supabase()

    st.sidebar.header("Account")
    mode = st.sidebar.radio("Mode", ["Login", "Sign up"], horizontal=True)

    email = st.sidebar.text_input("Email").strip().lower()
    password = st.sidebar.text_input("Password", type="password")

    if mode == "Sign up":
        if st.sidebar.button("Create account", use_container_width=True):
            sb.auth.sign_up({"email": email, "password": password})
            st.sidebar.success("Account created. Switch to Login.")
        return None

    if st.sidebar.button("Log in", use_container_width=True):
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["sb_user"] = res.user.model_dump()
        st.session_state["sb_session"] = res.session.model_dump()

    return st.session_state.get("sb_user")

def logout_ui():
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state.pop("sb_user", None)
        st.session_state.pop("sb_session", None)
        st.rerun()

def ensure_profile():
    sb = get_supabase()
    user = st.session_state.get("sb_user")
    if not user:
        return

    uid = user["id"]
    email = (user.get("email") or "").strip().lower()

    existing = sb.table("profiles").select("*").eq("user_id", uid).execute().data
    if existing:
        # Auto-promote creator if email matches
        if email == creator_email() and existing[0].get("role") != "creator":
            sb.table("profiles").update({"role": "creator"}).eq("user_id", uid).execute()
        return

    role = "creator" if email == creator_email() else "athlete"
    sb.table("profiles").insert({
        "user_id": uid,
        "email": email,
        "role": role,
        "sex": "Male",
        "experience": "Very experienced",
        "event_focus": "5000 m"
    }).execute()

def get_my_role() -> str:
    sb = get_supabase()
    user = st.session_state.get("sb_user")
    if not user:
        return "anonymous"
    prof = sb.table("profiles").select("role").eq("user_id", user["id"]).execute().data
    return prof[0]["role"] if prof else "athlete"
