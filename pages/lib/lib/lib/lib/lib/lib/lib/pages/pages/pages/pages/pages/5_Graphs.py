import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lib.auth import ensure_profile, logout_ui
from lib.db import recent_sessions, metrics_for_sessions

st.title("Graphs")

user = st.session_state.get("sb_user")
if not user:
    st.warning("Please log in.")
    st.stop()

ensure_profile()
logout_ui()

sessions = recent_sessions(user["id"], limit=200)
sids = [s["id"] for s in sessions]
mets = metrics_for_sessions(sids)

if not mets:
    st.info("Log some sessions to see graphs.")
    st.stop()

df = pd.DataFrame(mets).sort_values("session_id")

st.subheader("sRPE Load (by session)")
fig = plt.figure()
plt.plot(df["session_id"], df["sRPE_load"])
st.pyplot(fig)

st.subheader("Density score (by session)")
fig2 = plt.figure()
plt.plot(df["session_id"], df["density_score"])
st.pyplot(fig2)

st.subheader("Readiness modifier (by session)")
fig3 = plt.figure()
plt.plot(df["session_id"], df["readiness_modifier"])
st.pyplot(fig3)
