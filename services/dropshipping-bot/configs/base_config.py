import os
from dotenv import load_dotenv

# Load global .env file
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
