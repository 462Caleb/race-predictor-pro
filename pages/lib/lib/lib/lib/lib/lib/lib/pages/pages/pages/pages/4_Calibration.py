import streamlit as st
from lib.auth import ensure_profile, logout_ui

st.title("Calibration (Coming Next)")

user = st.session_state.get("sb_user")
if not user:
    st.warning("Please log in.")
    st.stop()

ensure_profile()
logout_ui()

st.info("Next upgrade: enter PRs (800/1600/5K etc.) and auto-tune ensemble weights.")
