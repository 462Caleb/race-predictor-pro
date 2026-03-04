import streamlit as st
from lib.auth import login_ui, ensure_profile, logout_ui, get_my_role

st.set_page_config(page_title="Race Predictor V2", layout="wide")

user = st.session_state.get("sb_user")

if not user:
    st.title("Race Predictor V2")
    st.caption("Log in or sign up using the sidebar.")
    login_ui()
    st.stop()

ensure_profile()
role = get_my_role()

st.sidebar.success(f"Logged in: {user.get('email')}")
st.sidebar.info(f"Role: {role}")
logout_ui()

st.title("Race Predictor V2")
st.caption("Use the sidebar to switch pages.")
