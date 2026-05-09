import os
import logging
from dotenv import load_dotenv
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load data from .env file
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TEMP_FOLDER = 'temp_images'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

async def convert_to_webp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return

    photo = await update.message.photo[-1].get_file()
    input_path = os.path.join(TEMP_FOLDER, f"{photo.file_id}.jpg")
    output_path = os.path.join(TEMP_FOLDER, f"{photo.file_id}.webp")

    await update.message.reply_text("Processing your photo to WebP... 🔄")

    try:
        await photo.download_to_drive(input_path)
        
        with Image.open(input_path) as img:
            # High quality WebP conversion
            img.save(output_path, "WEBP", quality=50)
        
        with open(output_path, 'rb') as webp_file:
            await update.message.reply_document(
                document=webp_file, 
                filename="hasil_foto.webp",
                caption="Ini versi webp buat portofolio kamu!",
                disable_content_type_detection=True
            )
            
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, convert_to_webp))
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()
