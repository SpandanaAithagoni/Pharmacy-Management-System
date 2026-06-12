import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class SupabaseConfig:

    def __init__(self):

        self.url = (
            os.getenv("SUPABASE_URL")
            or st.secrets.get("SUPABASE_URL")
        )

        self.key = (
            os.getenv("SUPABASE_KEY")
            or st.secrets.get("SUPABASE_KEY")
        )

        if not self.url or not self.key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY are missing"
            )

    def get_client(self) -> Client:

        return create_client(
            self.url,
            self.key
        )


def get_supabase() -> Client:

    return SupabaseConfig().get_client()
