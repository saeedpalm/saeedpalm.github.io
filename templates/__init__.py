import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the ESPNFantasyFootballClient class
from .api import ESPNFantasyFootballClient

# Initialize the API client
client = ESPNFantasyFootballClient()