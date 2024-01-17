import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.urandom(32)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    UPLOAD_FOLDER = "static/files"
    MONGODB_SETTINGS = {"db": "FlashcardAI"}
