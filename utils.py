import re

def format_telegram_message(text: str) -> str:
    """Format the message for Telegram with proper HTML formatting."""
    # Replace markdown links with HTML links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Replace markdown bold with HTML bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    
    # Replace markdown italic with HTML italic
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    
    # Replace markdown code with HTML code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Format lists with emojis
    text = re.sub(r'^\s*[-*]\s+(.+)$', r'• \1', text, flags=re.MULTILINE)
    
    # Format headers with bold and emojis
    text = re.sub(r'^#+\s+(.+)$', r'<b>📌 \1</b>', text, flags=re.MULTILINE)
    
    # Format contact information
    text = re.sub(r'(\w+@\w+\.\w+)', r'<code>\1</code>', text)
    
    # Format office locations
    text = re.sub(r'Office:\s*([^,\n]+)', r'🏢 <b>Office:</b> \1', text)
    
    # Format email addresses
    text = re.sub(r'Email:\s*([^,\n]+)', r'📧 <b>Email:</b> \1', text)
    
    # Format LinkedIn links
    text = re.sub(r'LinkedIn:\s*([^,\n]+)', r'🔗 <b>LinkedIn:</b> \1', text)
    
    # Format credit hours
    text = re.sub(r'Credit Hours:\s*([^,\n]+)', r'📚 <b>Credit Hours:</b> \1', text)
    
    # Format phone numbers
    text = re.sub(r'Phone:\s*([^,\n]+)', r'📞 <b>Phone:</b> \1', text)
    
    # Format course titles
    text = re.sub(r'\*\*([^*]+)\*\*:\s*', r'📖 <b>\1</b>\n', text)
    
    # Ensure proper line breaks
    text = text.replace('\n\n', '\n')
    
    # Add section separators
    text = re.sub(r'^([A-Z][a-z\s]+:)$', r'<b>🔹 \1</b>', text, flags=re.MULTILINE)
    
    return text 