from postgrest import APIResponse
from supabase import Client, create_client
from typing import Optional, Any


class SurveyRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase

# TODO