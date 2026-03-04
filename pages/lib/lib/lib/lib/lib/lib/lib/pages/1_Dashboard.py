import streamlit as st
import pandas as pd
from lib.auth import ensure_profile, logout_ui
from lib.db import my_profile, recent_sessions, metrics_for_sessions
from lib.predictors import predict_all, RACES
from lib.confidence import band

st.title("Dashboard")

user = st.session_state.get("sb_user")
if not user:
    st.warning("Please log in.")
    st.stop()

ensure_profile()
logout_ui()

profile = my_profile(user["id"])
st.caption(f"Profile: {profile.get('sex','—')} | Focus: {profile.get('event_focus','—')}")

c1, c2 = st.columns(2)
with c1:
    anchor_name = st.selectbox("Anchor race", list(RACES.keys()), index=5)
with c2:
    anchor_time = st.text_input("Anchor time (mm:ss or hh:mm:ss)", value="16:30")

def parse_time(t: str) -> float:
    parts = t.strip().split(":")
    try:
        parts = [float(p) for p in parts]
    except:
        return 0.0
    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    if len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s
    return 0.0

anchor_time_sec = parse_time(anchor_time)
anchor_dist_m = float(RACES[anchor_name])

sessions = recent_sessions(user["id"], limit=60)
sids = [s["id"] for s in sessions]
mets = metrics_for_sessions(sids)
dfm = pd.DataFrame(mets) if mets else pd.DataFrame()

readiness = 0.0
if not dfm.empty and "readiness_modifier" in dfm.columns:
    readiness = float(dfm.sort_values("session_id", ascending=False).iloc[0]["readiness_modifier"])

exp = st.slider("Riegel exponent (baseline)", 1.00, 1.10, 1.06, 0.01)

if anchor_time_sec > 0:
    preds = predict_all(anchor_dist_m, anchor_time_sec, exp=exp, readiness_modifier=readiness)

    weeks_of_data = 0
    if sessions:
        # rough proxy: number of unique weeks represented in last 60 sessions
        dates = pd.to_datetime([s["session_date"] for s in sessions], errors="coerce")
        weeks_of_data = int(dates.dt.isocalendar().week.nunique()) if dates.notna().any() else 0
        weeks_of_data = max(0, min(12, weeks_of_data))

    load_vol = float(dfm["sRPE_load"].std()) if (not dfm.empty and "sRPE_load" in dfm.columns) else 0.0

    def nice_time(sec: float) -> str:
        sec = float(sec)
        if sec >= 3600:
            h = int(sec // 3600); sec -= h*3600
            m = int(sec // 60); sec -= m*60
            return f"{h}:{m:02d}:{sec:04.1f}"
        m = int(sec // 60); sec -= m*60
        return f"{m}:{sec:04.1f}"

    rows = []
    for race, t in preds.items():
        lo, hi = band(t, weeks_of_data=weeks_of_data, load_volatility=load_vol, readiness_modifier=readiness)
        rows.append({
            "Race": race,
            "Predicted": nice_time(t),
            "Range": f"{nice_time(lo)} – {nice_time(hi)}"
        })

    st.subheader("Predictions")
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.caption(f"Readiness modifier (from latest notes): {readiness:+.3f}  |  Weeks of data: {weeks_of_data}")
else:
    st.info("Enter a valid anchor time to see predictions.")
