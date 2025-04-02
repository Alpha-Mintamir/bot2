import logging
from telegram import Update
from telegram.ext import ContextTypes
from utils import format_telegram_message
import requests
from config import API_KEY, BASE_URL

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = """
<b>👋 Welcome to the AAU Information Systems Chatbot!</b>

I'm here to help you explore the Information Systems department at Addis Ababa University. You can ask me about:

📚 Course information
👨‍🏫 Faculty members
🎉 Department events
🏢 Campus location
📞 Contact details
And much more!

Use /help to see available commands.
"""
    await update.message.reply_text(
        text=welcome_message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_message = """
<b>🤖 Available Commands:</b>

/start - Start the bot
/help - Show this help message

<b>📚 You can ask me about:</b>

• Course details and curriculum
• Faculty members and their contact information
• Department events and activities
• Campus location and facilities
• Admission requirements
• Career opportunities

Just type your question and I'll help you find the information you need!
"""
    await update.message.reply_text(
        text=help_message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages."""
    try:
        user_message = update.message.text
        logger.info(f"Received message: {user_message}")

        # Create a more focused prompt that includes the user's question
        prompt = f"""Based on the following system knowledge, please answer this question: {user_message}

If the question is about:
- Courses: Provide specific course details including credit hours
- Faculty: Give their office location, email, and LinkedIn if available
- Events: List relevant department events
- Location: Provide specific building and room information
- Contact: Give direct contact information

Keep responses concise but informative. If the information isn't in the knowledge base, say so politely."""

        # Make the API request
        headers = {
            'Content-Type': 'application/json',
        }
        
        params = {
            'key': API_KEY
        }
        
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "systemInstruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            }
        }
        
        response = requests.post(
            BASE_URL, 
            headers=headers, 
            params=params,
            json=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']

        # Format the response for Telegram
        formatted_text = format_telegram_message(generated_text)
        
        # Send the formatted message
        await update.message.reply_text(
            text=formatted_text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        logger.error(traceback.format_exc())
        await update.message.reply_text(
            "I apologize, but I encountered an error processing your message. Please try again later."
        ) 