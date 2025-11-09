"""
Beautifully formatted messages for Telegram bot.
Professional design for Fiverr demo.
"""
from typing import List, Dict, Any
from datetime import datetime

def format_welcome_message(user_name: str, is_new: bool = True) -> str:
    """Welcome message"""
    if is_new:
        return f"""
🎉 <b>Welcome, {user_name}!</b>

I am <b>AI Business Intelligence Agent</b> 🤖
Your personal assistant for document and data analysis.

<b>What I can do:</b>
📄 Analyze PDF, Excel, Word documents
🎤 Transcribe audio and voice messages
🌐 Parse and analyze web pages
💬 Answer questions about your documents
📊 Create visualizations and reports

<b>Quick start:</b>
1️⃣ Upload document or send URL
2️⃣ Wait for analysis completion
3️⃣ Ask questions about content

💡 <i>Tip: use /help for detailed information</i>
"""
    else:
        return f"""
👋 <b>Welcome back, {user_name}!</b>

Ready to continue working with your documents! 📚

Use menu below for quick access to features.
"""

def format_stats_message(stats: Dict[str, Any]) -> str:
    """User statistics"""
    return f"""
📊 <b>Your Statistics</b>

<b>Documents:</b>
📄 Total documents: {stats.get('total_docs', 0)}
📌 Active document: {stats.get('active_doc', 'None')}
📈 Processed this month: {stats.get('docs_this_month', 0)}

<b>AI Usage:</b>
💬 Questions asked: {stats.get('questions_asked', 0)}
⏱️ Average response time: {stats.get('avg_response_time', 'N/A')} sec
🎯 Answer accuracy: {stats.get('accuracy', 95)}%

<b>Document types:</b>
📄 PDF: {stats.get('pdf_count', 0)}
📊 Excel: {stats.get('excel_count', 0)}
📝 Word: {stats.get('word_count', 0)}
🌐 URL: {stats.get('url_count', 0)}
🎤 Audio: {stats.get('audio_count', 0)}

<b>Activity:</b>
📅 First visit: {stats.get('first_visit', 'N/A')}
🕒 Last activity: {stats.get('last_activity', 'N/A')}
🔥 Streak: {stats.get('streak_days', 0)} days in a row!

{"💎 <b>Premium status: Active</b>" if stats.get('is_premium') else "✨ <i>Get Premium for extended features!</i>"}
"""

def format_document_info(doc: Dict[str, Any]) -> str:
    """Document information"""
    doc_type_icons = {
        'pdf': '📄',
        'excel': '📊',
        'word': '📝',
        'url': '🌐',
        'audio': '🎤',
    }

    icon = doc_type_icons.get(doc.get('type', '').lower(), '📎')
    size = doc.get('size', 0)
    size_str = f"{size / 1024:.1f} KB" if size < 1024*1024 else f"{size / (1024*1024):.1f} MB"

    return f"""
{icon} <b>{doc.get('name', 'Untitled')}</b>

<b>Information:</b>
📝 Type: {doc.get('type', 'Unknown')}
📏 Size: {size_str}
📊 Characters: {doc.get('char_count', 0):,}
📅 Uploaded: {doc.get('created_at', 'N/A')}

<b>Analysis:</b>
✅ Status: {"Processed" if doc.get('processed') else "Processing..."}
💬 Questions asked: {doc.get('questions_count', 0)}
⭐ Rating: {'⭐' * doc.get('rating', 0)}

{doc.get('summary', '<i>Summary not yet available</i>')}
"""

def format_document_list(documents: List[Dict[str, Any]], page: int = 1, per_page: int = 5) -> str:
    """Document list"""
    if not documents:
        return """
📭 <b>You have no documents yet</b>

Upload your first document:
• 📄 PDF file
• 📊 Excel spreadsheet
• 📝 Word document
• 🌐 Web page URL
• 🎤 Audio recording

Or use /help command for detailed information.
"""

    total = len(documents)
    start = (page - 1) * per_page
    end = start + per_page
    page_docs = documents[start:end]

    result = f"📚 <b>Your Documents</b> (Total: {total})\n\n"

    for idx, doc in enumerate(page_docs, start=start+1):
        icon = {'pdf': '📄', 'excel': '📊', 'word': '📝', 'url': '🌐', 'audio': '🎤'}.get(
            doc.get('type', '').lower(), '📎'
        )
        active = " ✅" if doc.get('is_active') else ""
        result += f"{idx}. {icon} <b>{doc.get('name', 'Untitled')}</b>{active}\n"
        result += f"   📅 {doc.get('created_at', 'N/A')} | 💬 {doc.get('questions_count', 0)} questions\n\n"

    if total > per_page:
        result += f"\n📄 Page {page} of {(total + per_page - 1) // per_page}"

    return result

def format_help_message() -> str:
    """Help guide"""
    return """
❓ <b>Usage Guide</b>

<b>📄 Working with Documents</b>

<b>Upload:</b>
• Send PDF, Excel or Word file
• Send web page URL
• Send voice message or audio file

<b>Analysis:</b>
• Bot automatically processes document
• Extracts text and data structure
• Makes document active for questions

<b>💬 Document Questions</b>

Simply write your question, for example:
• "What are the main conclusions?"
• "How many total records?"
• "Summarize content"
• "Find information about..."

<b>📊 Additional Features</b>

/start - Start working
/mydocs - List all documents
/clear - Delete all documents
/stats - Usage statistics
/settings - Bot settings
/help - This help

<b>💎 Premium Features</b>

• 📈 Data visualization from Excel
• 📥 Export results (PDF/Excel/Word)
• 🔍 Extended document analysis
• ⚡ Priority processing
• 📊 Detailed analytics

<b>🆘 Need help?</b>
Contact us: support@example.com
"""

def format_processing_message(file_name: str, file_type: str) -> str:
    """Processing message"""
    icons = {
        'pdf': '📄',
        'excel': '📊',
        'word': '📝',
        'url': '🌐',
        'audio': '🎤',
    }
    icon = icons.get(file_type.lower(), '📎')

    return f"""
{icon} <b>Processing document...</b>

📝 File: {file_name}
⏳ Status: Analyzing...

This may take some time depending on document size.
You will receive notification after processing completion.

💡 <i>You can continue working with other documents</i>
"""

def format_success_message(file_name: str, stats: Dict[str, Any]) -> str:
    """Successful processing message"""
    return f"""
✅ <b>Document processed successfully!</b>

📝 {file_name}
📊 Characters extracted: {stats.get('char_count', 0):,}
⏱️ Processing time: {stats.get('processing_time', 'N/A')} sec

Document set as active for dialogue.
Now you can ask questions about it! 💬

<b>What's next?</b>
• Ask question about content
• Get summary
• Extract key data
• Create report or visualization
"""

def format_error_message(error_type: str, details: str = "") -> str:
    """Error message"""
    messages = {
        'file_too_large': '📦 File too large. Maximum size: 50 MB.',
        'unsupported_format': '❌ Unsupported file format.',
        'processing_error': '⚠️ Error processing document.',
        'database_error': '🗄️ Database error. Try again later.',
        'api_error': '🔌 Error connecting to AI service.',
        'no_active_document': '📭 No active document. Upload document first.',
        'network_error': '🌐 Network error. Check connection.',
    }

    message = messages.get(error_type, '❌ Unknown error occurred.')

    if details:
        message += f"\n\n<i>Details: {details}</i>"

    message += "\n\n💡 <i>Try again or contact support</i>"

    return message

def format_premium_promo() -> str:
    """Premium subscription promo"""
    return """
✨ <b>Upgrade to Premium!</b>

<b>Get more features:</b>

📈 <b>Extended Analytics</b>
   • Data visualization
   • Automatic charts and diagrams
   • Export in any format

🚀 <b>Priority Processing</b>
   • 3x faster
   • No queue

💎 <b>Higher Limits</b>
   • Up to 100 documents (vs 10)
   • Up to 50 MB files (vs 10 MB)
   • Unlimited questions

🎯 <b>Advanced AI</b>
   • More accurate answers
   • Deep analysis
   • Multi-document search

<b>💰 Pricing:</b>
📅 Monthly: $9.99
📅 Yearly: $89.99 (-25%)
🎁 Trial period: 7 days free

<i>Click "Buy Premium" to start!</i>
"""

def format_comparison_table() -> str:
    """Pricing comparison table"""
    return """
📋 <b>Plan Comparison</b>

<b>FREE</b>
• 10 documents
• 10 MB max size
• Basic AI
• Standard speed
• No export

<b>PREMIUM</b> 💎
• 100 documents
• 50 MB max size
• Advanced AI
• Priority processing
• Export to PDF/Excel/Word
• Data visualization
• 24/7 email support

<b>ENTERPRISE</b> 🏢
• Unlimited documents
• 500 MB max size
• Custom AI models
• Instant processing
• API access
• Custom integration
• Personal manager

Contact us for Enterprise plan!
"""
