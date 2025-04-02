import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes
from utils import format_telegram_message
import requests
from config import API_KEY, BASE_URL, SYSTEM_PROMPT

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
        
        # Log API key presence (without revealing the actual key)
        logger.info(f"API_KEY present: {bool(API_KEY)}")
        
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
        
        logger.info("Sending request to Gemini API")
        
        response = requests.post(
            BASE_URL, 
            headers=headers, 
            params=params,
            json=data,
            timeout=30
        )
        
        logger.info(f"Gemini API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"API error: {response.text}")
            raise Exception(f"API returned status code {response.status_code}: {response.text}")
            
        result = response.json()
        logger.info("Successfully parsed JSON response")
        
        # Check if the response has the expected structure
        if 'candidates' not in result:
            logger.error(f"Unexpected API response structure: {result}")
            raise Exception("API response doesn't contain 'candidates'")
            
        if not result['candidates']:
            logger.error("API returned empty candidates list")
            raise Exception("API returned empty candidates list")
            
        if 'content' not in result['candidates'][0]:
            logger.error(f"Missing 'content' in first candidate: {result['candidates'][0]}")
            raise Exception("API response doesn't contain 'content' in first candidate")
            
        if 'parts' not in result['candidates'][0]['content']:
            logger.error(f"Missing 'parts' in content: {result['candidates'][0]['content']}")
            raise Exception("API response doesn't contain 'parts' in content")
            
        if not result['candidates'][0]['content']['parts']:
            logger.error("Empty 'parts' list in content")
            raise Exception("API response contains empty 'parts' list")
            
        if 'text' not in result['candidates'][0]['content']['parts'][0]:
            logger.error(f"Missing 'text' in first part: {result['candidates'][0]['content']['parts'][0]}")
            raise Exception("API response doesn't contain 'text' in first part")
        
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        logger.info("Successfully extracted text from API response")

        # Format the response for Telegram
        formatted_text = format_telegram_message(generated_text)
        logger.info("Text formatted for Telegram")
        
        # Send the formatted message
        await update.message.reply_text(
            text=formatted_text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        logger.info("Response sent to user")

    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        logger.error(traceback.format_exc())
        await update.message.reply_text(
            "I apologize, but I encountered an error processing your message. Please try again later."
        ) 