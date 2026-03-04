import pandas as pd
from lib.supabase_client import get_supabase

def my_profile(user_id: str) -> dict:
    sb = get_supabase()
    data = sb.table("profiles").select("*").eq("user_id", user_id).execute().data
    return data[0] if data else {}

def list_profiles():
    sb = get_supabase()
    return sb.table("profiles").select("user_id,email,role,sex,event_focus").execute().data

def insert_session(user_id: str, session_date: str, session_type: str, effort: int, notes: str) -> int:
    sb = get_supabase()
    res = sb.table("sessions").insert({
        "user_id": user_id,
        "session_date": session_date,
        "session_type": session_type,
        "effort": effort,
        "notes": notes
    }).execute()
    return res.data[0]["id"]

def insert_intervals(session_id: int, intervals_df: pd.DataFrame):
    sb = get_supabase()
    rows = intervals_df.to_dict(orient="records")
    for r in rows:
        r["session_id"] = session_id
    if rows:
        sb.table("intervals").insert(rows).execute()

def upsert_metrics(session_id: int, metrics: dict):
    sb = get_supabase()
    sb.table("session_metrics").upsert({"session_id": session_id, **metrics}).execute()

def recent_sessions(user_id: str, limit: int = 60):
    sb = get_supabase()
    return sb.table("sessions").select("*").eq("user_id", user_id).order("session_date", desc=True).limit(limit).execute().data

def metrics_for_sessions(session_ids):
    sb = get_supabase()
    if not session_ids:
        return []
    return sb.table("session_metrics").select("*").in_("session_id", session_ids).execute().data

def upsert_week(user_id: str, week_start: str, planned_miles: float, actual_miles: float, phase: str, notes: str):
    sb = get_supabase()
    sb.table("training_weeks").upsert({
        "user_id": user_id,
        "week_start": week_start,
        "planned_miles": planned_miles,
        "actual_miles": actual_miles,
        "phase": phase,
        "notes": notes
    }).execute()

def weeks(user_id: str, limit: int = 24):
    sb = get_supabase()
    return sb.table("training_weeks").select("*").eq("user_id", user_id).order("week_start", desc=True).limit(limit).execute().data
