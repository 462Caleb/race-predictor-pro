import os
from supabase import create_client

def get_supabase():
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_ANON_KEY"]
    )

def creator_email():
    return os.environ.get("CREATOR_EMAIL","").lower()
