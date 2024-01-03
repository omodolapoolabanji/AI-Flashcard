import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
