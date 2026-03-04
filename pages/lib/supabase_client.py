import os
from supabase import create_client, Client

def get_supabase() -> Client:
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"])

def creator_email() -> str:
    return os.environ.get("CREATOR_EMAIL", "").strip().lower()
