import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration loaded from environment variables"""
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:3000/api/auth/callback")
    
    # Anthropic API Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Gmail API Scopes
    GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    
    # Google OAuth Client Configuration
    @staticmethod
    def get_google_client_config():
        """Returns the Google OAuth client configuration"""
        return {
            "web": {
                "client_id": Config.GOOGLE_CLIENT_ID,
                "client_secret": Config.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [Config.REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }

# Create a singleton instance
config = Config()
