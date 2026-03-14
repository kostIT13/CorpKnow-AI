import os 
from dotenv import load_dotenv
from typing import Optional


load_dotenv()


DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")