import os
from dotenv import load_dotenv

load_dotenv(override=True)

GROQ_API_URL = os.getenv('GROQ_API_URL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
LLMMODEL = os.getenv('LLMMODEL')

REQUIRED_FIELDS = os.getenv('REQUIRED_FIELDS', '').split(',')