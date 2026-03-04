from lib.supabase_client import get_supabase

def insert_session(user_id, session_date, session_type, effort, notes):
    sb = get_supabase()

    res = sb.table("sessions").insert({
        "user_id": user_id,
        "session_date": session_date,
        "session_type": session_type,
        "effort": effort,
        "notes": notes
    }).execute()

    return res.data[0]["id"]
