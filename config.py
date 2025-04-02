import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Gemini API Configuration
API_KEY = os.getenv('GEMINI_API_KEY')
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Webhook URL (for Render deployment)
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-render-domain.onrender.com')

# Add validation
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!") 