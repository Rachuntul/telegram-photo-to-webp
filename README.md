# 📸 Telegram Photo-to-WebP Converter Bot

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-blue?style=for-the-badge&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A lightweight and efficient Telegram bot designed to automatically convert images (JPG/PNG) into the **WebP** format. Perfect for photographers and web developers looking to optimize image assets without losing quality.

---

## 🌟 Key Features
- **⚡ Instant Conversion**: Send any photo and receive a `.webp` document immediately.
- **🖼️ Web-Optimized**: Uses `Pillow` to balance high visual quality with significant file size reduction.
- **🧹 Auto-Cleanup**: Temporary processing files are deleted instantly to save server space.
- **🔒 Privacy First**: Zero permanent storage. Your images are yours alone.
- **🤖 Smart Rendering**: Bypasses Telegram's auto-sticker rendering by sending as a raw document.

## 🛠️ Tech Stack
- **Core:** Python 3.x
- **API:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- **Image Engine:** [Pillow (PIL)](https://python-pillow.org/)
- **Environment:** `python-dotenv` for secure configuration.

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Rachuntul/telegram-photo-to-webp.git](https://github.com/Rachuntul/telegram-photo-to-webp.git
cd telegram-photo-to-webp

```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configuration

Create a `.env` file in the root directory:

```bash
touch .env

```

Add your bot token from [@BotFather](https://t.me/botfather) inside the `.env` file:

```text
BOT_TOKEN=your_token_here

```

### 5. Launch the Bot

```bash
python3 converter.py

```

---

## 📸 Usage

1. Open a chat with your bot on Telegram.
2. Send an image as a **"Photo"**.
3. The bot will automatically reply with the **.webp** version as a document.

## 📝 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

*Developed by [Dion Puji Ramdani*](https://www.google.com/search?q=https://github.com/Rachuntul)
