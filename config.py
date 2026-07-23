import os
from dotenv import load_dotenv

load_dotenv()
TEL_TOKEN = os.getenv("TEL_TOKEN")
API_URL = os.getenv("API_URL")