import streamlit as st
import pandas as pd
from datetime import date
from lib.auth import ensure_profile, logout_ui
from lib.notes_rules import analyze_notes
from lib.metrics import compute_metrics
from lib.db import insert_session, insert_intervals, upsert_metrics

st.title("Log Training")

user = st.session_state.get("sb_user")
if not user:
    st.warning("Please log in.")
    st.stop()

ensure_profile()
logout_ui()

c1, c2, c3 = st.columns(3)
with c1:
    session_date = st.date_input("Date", value=date.today())
with c2:
    session_type = st.selectbox("Session type", ["Easy", "Long", "Tempo", "Track", "Race", "Other"])
with c3:
    effort = st.slider("Effort (1–10)", 1, 10, 6)

notes = st.text_area("Notes (optional)", placeholder="Example: calves sore, heavy legs, felt great, etc.")
analysis = analyze_notes(notes)

if analysis["guidance"]:
    st.warning("Notes-based guidance (rule-based):")
    for g in analysis["guidance"]:
        st.write("• " + g)

st.subheader("Intervals (optional)")
st.caption("Use this for structured workouts. Leave empty for easy/long runs if you want.")

default = pd.DataFrame([{
    "sets": 1,
    "reps_per_set": 6,
    "rep_distance_m": 800,
    "rep_time_sec": 150,
    "rest_rep_sec": 90,
    "rest_set_sec": 0
}])

intervals = st.data_editor(default, num_rows="dynamic", use_container_width=True)

if st.button("Save session", type="primary"):
    sid = insert_session(
        user_id=user["id"],
        session_date=str(session_date),
        session_type=session_type,
        effort=int(effort),
        notes=notes
    )

    intervals_clean = pd.DataFrame()
    if intervals is not None and not intervals.empty:
        intervals_clean = intervals.dropna()

    if not intervals_clean.empty:
        insert_intervals(sid, intervals_clean)
        metrics = compute_metrics(intervals_clean, effort=int(effort), notes_analysis=analysis)
    else:
        metrics = compute_metrics(pd.DataFrame(), effort=int(effort), notes_analysis=analysis)

    upsert_metrics(sid, metrics)
    st.success("Saved!")
