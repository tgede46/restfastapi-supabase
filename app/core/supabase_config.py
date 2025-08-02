import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.url or not self.anon_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
    
    def get_client(self) -> Client:
        """Retourne un client Supabase configuré"""
        return create_client(self.url, self.anon_key)
    
    def get_admin_client(self) -> Client:
        """Retourne un client Supabase avec les droits administrateur"""
        if not self.service_role_key:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY must be set for admin operations")
        return create_client(self.url, self.service_role_key)

# Instance globale
supabase_config = SupabaseConfig()
