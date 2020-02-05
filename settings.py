# settings.py
from dotenv import load_dotenv
import os
load_dotenv()

AUTHORIZATION_TOKEN = os.getenv("AUTHORIZATION_TOKEN")