import os
import logging
import subprocess
import numpy as np
from dotenv import load_dotenv
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CallbackQueryHandler, filters

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
TEMP_FOLDER = 'temp_images'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# --- FUNGSI FILTER WARNA & EFEK ---
def apply_dslr_filter(img, filter_type):
    if filter_type == "vibrant_chrome":
        enhancer_col = ImageEnhance.Color(img)
        img = enhancer_col.enhance(1.4)
        enhancer_con = ImageEnhance.Contrast(img)
        return enhancer_con.enhance(1.2)
        
    elif filter_type == "teal_orange":
        img_np = np.array(img).astype(float)
        img_np[:,:,0] = np.clip(img_np[:,:,0] * 1.2, 0, 255) 
        img_np[:,:,2] = np.clip(img_np[:,:,2] * 1.1, 0, 255) 
        return Image.fromarray(img_np.astype('uint8'))
        
    elif filter_type == "monochrome":
        img = img.convert("L")
        enhancer_con = ImageEnhance.Contrast(img)
        return enhancer_con.enhance(1.5)

    elif filter_type == "vintage_sepia":
        # Rumus matrix warna Sepia
        img_np = np.array(img).astype(float)
        tr = np.clip(0.393 * img_np[:,:,0] + 0.769 * img_np[:,:,1] + 0.189 * img_np[:,:,2], 0, 255)
        tg = np.clip(0.349 * img_np[:,:,0] + 0.686 * img_np[:,:,1] + 0.168 * img_np[:,:,2], 0, 255)
        tb = np.clip(0.272 * img_np[:,:,0] + 0.534 * img_np[:,:,1] + 0.131 * img_np[:,:,2], 0, 255)
        img_np[:,:,0], img_np[:,:,1], img_np[:,:,2] = tr, tg, tb
        return Image.fromarray(img_np.astype('uint8'))

    elif filter_type == "cyberpunk":
        # Menaikkan Biru & Merah, Menurunkan Hijau (High Contrast)
        img_np = np.array(img).astype(float)
        img_np[:,:,0] = np.clip(img_np[:,:,0] * 1.3, 0, 255) 
        img_np[:,:,1] = np.clip(img_np[:,:,1] * 0.8, 0, 255) 
        img_np[:,:,2] = np.clip(img_np[:,:,2] * 1.4, 0, 255) 
        img = Image.fromarray(img_np.astype('uint8'))
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.3)

    elif filter_type == "pencil_sketch":
        # Mengubah ke hitam putih, deteksi tepi, lalu dibalik warnanya
        img = img.convert("L")
        img = img.filter(ImageFilter.FIND_EDGES)
        return ImageOps.invert(img)

    elif filter_type == "posterize":
        # Mengurangi bit kedalaman warna
        return ImageOps.posterize(img, bits=3)

    return img

# --- HANDLE FOTO MASUK ---
async def handle_incoming_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        file_obj = await update.message.document.get_file()
        original_name = os.path.splitext(update.message.document.file_name)[0]
    elif update.message.photo:
        file_obj = await update.message.photo[-1].get_file()
        original_name = f"photo_{update.message.photo[-1].file_unique_id}"
    else:
        return

    input_path = os.path.join(TEMP_FOLDER, f"{file_obj.file_id}.jpg")
    context.user_data['input_path'] = input_path
    context.user_data['original_name'] = original_name

    await file_obj.download_to_drive(input_path)

    keyboard = [
        [InlineKeyboardButton("🔄 Convert Format Gambar", callback_data="menu_format")],
        [InlineKeyboardButton("📄 Convert ke Dokumen (PDF/Office)", callback_data="menu_docs")],
        [InlineKeyboardButton("🎨 Filter Warna & Efek", callback_data="menu_filter")],
        [InlineKeyboardButton("🚀 Upscale Gambar 2x", callback_data="process_upscale")]
    ]
    await update.message.reply_text("Pilih kategori aksi untuk fotomu: 🛠️", reply_markup=InlineKeyboardMarkup(keyboard))

# --- HANDLE KLIK MENU ---
async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action = query.data
    input_path = context.user_data.get('input_path')
    original_name = context.user_data.get('original_name')

    if not input_path or not os.path.exists(input_path):
        await query.edit_message_text("❌ File expired. Silakan kirim ulang fotonya.")
        return

    if action == "menu_format":
        keyboard = [
            [InlineKeyboardButton("WebP (Comp <100KB)", callback_data="convert_webp"), InlineKeyboardButton("PNG", callback_data="convert_png")],
            [InlineKeyboardButton("JPG", callback_data="convert_jpg"), InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")]
        ]
        await query.edit_message_text("Pilih format gambar tujuan:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif action == "menu_docs":
        keyboard = [
            [InlineKeyboardButton("PDF", callback_data="doc_pdf"), InlineKeyboardButton("Word (DOCX)", callback_data="doc_docx")],
            [InlineKeyboardButton("Excel (XLSX)", callback_data="doc_xlsx"), InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")]
        ]
        await query.edit_message_text("Pilih format dokumen tujuan:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif action == "menu_filter":
        # MENU FILTER DIPERLUAS
        keyboard = [
            [InlineKeyboardButton("Fujifilm Chrome", callback_data="fl_vibrant"), InlineKeyboardButton("Teal & Orange", callback_data="fl_teal")],
            [InlineKeyboardButton("Leica Mono", callback_data="fl_mono"), InlineKeyboardButton("Vintage Sepia", callback_data="fl_sepia")],
            [InlineKeyboardButton("Cyberpunk Neon", callback_data="fl_cyber"), InlineKeyboardButton("Pencil Sketch", callback_data="fl_sketch")],
            [InlineKeyboardButton("Pop Art Poster", callback_data="fl_poster"), InlineKeyboardButton("Efek Blur", callback_data="fl_blur")],
            [InlineKeyboardButton("⬅️ Kembali", callback_data="back_main")]
        ]
        await query.edit_message_text("Pilih efek filter foto:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    elif action == "back_main":
        keyboard = [
            [InlineKeyboardButton("🔄 Convert Format Gambar", callback_data="menu_format")],
            [InlineKeyboardButton("📄 Convert ke Dokumen (PDF/Office)", callback_data="menu_docs")],
            [InlineKeyboardButton("🎨 Filter Warna & Efek", callback_data="menu_filter")],
            [InlineKeyboardButton("🚀 Upscale Gambar 2x", callback_data="process_upscale")]
        ]
        await query.edit_message_text("Pilih kategori aksi untuk fotomu: 🛠️", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # --- PROSES EKSEKUSI ---
    await query.edit_message_text("Sedang memproses... Harap bersabar 🔄")
    output_path = None
    filename = ""

    try:
        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "P") and action not in ("convert_png", "doc_pdf", "doc_docx", "doc_xlsx"):
                img = img.convert("RGB")

            if action == "convert_webp":
                output_path = os.path.join(TEMP_FOLDER, f"{original_name}.webp")
                q = 90
                while q > 10:
                    img.save(output_path, "WEBP", quality=q)
                    if os.path.getsize(output_path) < 100 * 1024:
                        break
                    q -= 5
                filename = f"{original_name}.webp"

            elif action == "convert_png":
                output_path = os.path.join(TEMP_FOLDER, f"{original_name}.png")
                img.save(output_path, "PNG")
                filename = f"{original_name}.png"

            elif action == "convert_jpg":
                output_path = os.path.join(TEMP_FOLDER, f"{original_name}.jpg")
                img.save(output_path, "JPEG", quality=95)
                filename = f"{original_name}.jpg"

            # FILTER EKSEKUSI (DIPERLUAS)
            elif action in ("fl_vibrant", "fl_teal", "fl_mono", "fl_sepia", "fl_cyber", "fl_sketch", "fl_poster"):
                f_type_map = {
                    "fl_vibrant": "vibrant_chrome",
                    "fl_teal": "teal_orange",
                    "fl_mono": "monochrome",
                    "fl_sepia": "vintage_sepia",
                    "fl_cyber": "cyberpunk",
                    "fl_sketch": "pencil_sketch",
                    "fl_poster": "posterize"
                }
                f_type = f_type_map[action]
                filtered = apply_dslr_filter(img, f_type)
                output_path = os.path.join(TEMP_FOLDER, f"{original_name}_filter.jpg")
                filtered.save(output_path, "JPEG", quality=95)
                filename = f"{original_name}_{f_type}.jpg"

            elif action == "fl_blur":
                output_path = os.path.join(TEMP_FOLDER, f"{original_name}_blur.jpg")
                img.filter(ImageFilter.GaussianBlur(radius=7)).save(output_path, "JPEG", quality=90)
                filename = f"{original_name}_blur.jpg"

            elif action == "process_upscale":
                output_path = os.path.join(TEMP_FOLDER, f"{original_name}_upscaled.jpg")
                img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS).save(output_path, "JPEG", quality=95)
                filename = f"{original_name}_upscaled.jpg"

            elif action in ("doc_pdf", "doc_docx", "doc_xlsx"):
                temp_jpg = os.path.join(TEMP_FOLDER, f"thumb_{original_name}.jpg")
                img.save(temp_jpg, "JPEG")
                
                target_ext = "pdf" if action == "doc_pdf" else "docx" if action == "doc_docx" else "xlsx"
                
                cmd = f"libreoffice --headless --convert-to {target_ext} --outdir {TEMP_FOLDER} {temp_jpg}"
                subprocess.run(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                output_path = os.path.join(TEMP_FOLDER, f"thumb_{original_name}.{target_ext}")
                filename = f"{original_name}.{target_ext}"
                if os.path.exists(temp_jpg): os.remove(temp_jpg)

        if output_path and os.path.exists(output_path):
            with open(output_path, 'rb') as f:
                await query.message.reply_document(document=f, filename=filename, caption="✅ Berhasil diproses!", disable_content_type_detection=True)
            os.remove(output_path)

    except Exception as e:
        await query.message.reply_text(f"❌ Error: {e}")
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        await query.message.delete()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).read_timeout(60).connect_timeout(60).build()
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_incoming_photo))
    app.add_handler(CallbackQueryHandler(handle_menu_click))
    
    print("Bot Premium Multi-Converter siap dieksekusi...")
    app.run_polling()
