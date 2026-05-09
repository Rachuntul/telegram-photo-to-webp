# telegram-photo-to-webp
Simple Telegram Bot to convert PNG/JPG to WebP format using Python.

# 📸 Telegram Photo-to-WebP Converter Bot

A lightweight Telegram bot built with Python that automatically converts images (JPG/PNG) into the **WebP** format. Perfect for photographers and web developers looking to optimize image assets on the fly.

## 🌟 Features
- **Instant Conversion**: Send a photo, get a `.webp` document back immediately.
- **Optimized for Web**: Uses Pillow to maintain high visual quality while significantly reducing file size.
- **Auto-Cleanup**: Temporary files are automatically deleted after processing to keep your server storage clean.
- **Privacy Focused**: No images are stored permanently on the server.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Libraries**: `python-telegram-bot`, `Pillow` (PIL)
- **Deployment**: Can be run on any Linux server or via Docker.

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python installed on your system:
```bash
python3 --version
