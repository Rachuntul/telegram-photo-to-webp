import os
import logging
from dotenv import load_dotenv
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TEMP_FOLDER = 'temp_images'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Ensure temp directory exists
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

async def convert_to_webp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Determine if input is a Document or a Photo
    if update.message.document:
        file_obj = await update.message.document.get_file()
        # Get filename without extension
        original_name = os.path.splitext(update.message.document.file_name)[0]
    elif update.message.photo:
        file_obj = await update.message.photo[-1].get_file()
        original_name = f"photo_{update.message.photo[-1].file_unique_id}"
    else:
        return

    input_path = os.path.join(TEMP_FOLDER, f"{file_obj.file_id}.jpg")
    output_path = os.path.join(TEMP_FOLDER, f"{original_name}.webp")

    status_msg = await update.message.reply_text("Processing your photo to WebP... 🔄")

    try:
        # Download image from Telegram
        await file_obj.download_to_drive(input_path)
        
        with Image.open(input_path) as img:
            # --- AUTO RESIZE LOGIC ---
            max_width = 1920
            if img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(float(img.height) * float(ratio))
                img = img.resize((max_width, new_height), Image.LANCZOS)
            
            # Save as WebP
            img.save(output_path, "WEBP", quality=75)
        
        # Send the converted file back
        with open(output_path, 'rb') as webp_file:
            await update.message.reply_document(
                document=webp_file, 
                filename=f"{original_name}.webp",
                caption=f"✅ Converted: {original_name}.webp",
                disable_content_type_detection=True
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
    finally:
        # Cleanup: Delete status message and temporary files
        await status_msg.delete()
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    # Build application with custom timeouts
    app = ApplicationBuilder().token(TOKEN).read_timeout(30).connect_timeout(30).build()
    
    # Handle both Photos and Image Documents
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, convert_to_webp))
    
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()
