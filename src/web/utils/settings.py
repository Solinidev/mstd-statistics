import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

session_secret = os.getenv('SESSION_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
host = os.getenv('HOST')