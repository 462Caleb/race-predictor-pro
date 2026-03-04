import streamlit as st
import pandas as pd
from datetime import date, timedelta
from lib.auth import ensure_profile, logout_ui
from lib.db import upsert_week, weeks

st.title("Training Weeks")

user = st.session_state.get("sb_user")
if not user:
    st.warning("Please log in.")
    st.stop()

ensure_profile()
logout_ui()

today = date.today()
monday = today - timedelta(days=today.weekday())

c1, c2 = st.columns(2)
with c1:
    week_start = st.date_input("Week start (Monday)", value=monday)
with c2:
    phase = st.selectbox("Phase", ["Base", "Build", "Peak", "Taper"], index=1)

planned = st.number_input("Planned miles", 0.0, 200.0, 45.0, 1.0)
actual = st.number_input("Actual miles", 0.0, 200.0, 45.0, 1.0)
notes = st.text_area("Week notes (optional)")

if st.button("Save week", type="primary"):
    upsert_week(user["id"], str(week_start), planned, actual, phase, notes)
    st.success("Week saved.")

st.subheader("Recent weeks")
data = weeks(user["id"], limit=24)
st.dataframe(pd.DataFrame(data), use_container_width=True)
