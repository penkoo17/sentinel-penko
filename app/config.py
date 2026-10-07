import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SCAN_TIMEOUT = int(os.getenv("SCAN_TIMEOUT", "15"))
MAX_CRAWL_PAGES = int(os.getenv("MAX_CRAWL_PAGES", "20"))
MAX_CRAWL_DEPTH = int(os.getenv("MAX_CRAWL_DEPTH", "2"))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "0.5"))