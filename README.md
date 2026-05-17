<div align="center">

 <h1>Telegram Multi-Converter Bot</h1>
 <p>A powerful, lightweight, and Docker-optimized Telegram bot for image processing and document generation.</p>

 <a href="https://www.python.org/">
   <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
 </a>

 <a href="https://core.telegram.org/bots/api">
   <img src="https://img.shields.io/badge/Telegram_Bot_API-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
 </a>

 <a href="https://www.docker.com/">
   <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
 </a>

 <a href="LICENSE">
   <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" />
 </a>

 <a href="https://t.me/BotFather">
   <img src="https://img.shields.io/badge/Create_Bot-@BotFather-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
 </a>

</div>

---

# Key Features

<details>
<summary><b>Format Conversion</b></summary>
<br>

Convert images seamlessly to WebP (auto-compressed under 100KB), PNG, and JPG while maintaining visual quality.

</details>

<details>
<summary><b>Document Generation</b></summary>
<br>

Convert images directly into PDF, Word (DOCX), and Excel (XLSX) files using LibreOffice headless mode inside Docker.

</details>

<details>
<summary><b>Aesthetic Filters</b></summary>
<br>

Apply cinematic filters like Fujifilm Chrome, Teal & Orange, Leica Monochrome, Cyberpunk Neon, Pencil Sketch, and Vintage Sepia.

</details>

<details>
<summary><b>Upscaling Resolution</b></summary>
<br>

Upscale images up to 2x resolution using Lanczos resampling for sharper details.

</details>

<details>
<summary><b>RAM Disk Optimization</b></summary>
<br>

Uses Docker `tmpfs` RAM disk for ultra-fast temporary processing without slow disk bottlenecks.

</details>

---

# Tech Stack

- **Core**: Python 3.11
- **Framework**: `python-telegram-bot`
- **Image Processing**: Pillow (PIL), NumPy
- **Document Engine**: LibreOffice Headless
- **Deployment**: Docker & Docker Compose

---

# Quick Start Guide

## 1. Clone Repository

```bash
git clone https://github.com/Rachuntul/telegram-photo-to-webp.git
cd telegram-photo-to-webp
```

## 2. Configure Environment

Copy example environment file:

```bash
cp .env.example .env
```

Open `.env` and insert your Telegram bot token from BotFather:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

## 3. Run with Docker

```bash
docker compose up -d --build
```

---

# Usage

1. Start chat with your Telegram bot
2. Send image/photo
3. Choose action from inline menu
4. Wait a few seconds
5. Receive processed result instantly

---

# Support & Donate

If this project helps you, you can support development here:

<p align="left">
 <a href="https://saweria.co/RACHUNTUL">
   <img src="https://img.shields.io/badge/Donate-Saweria-orange?style=for-the-badge&logo=buymeacoffee&logoColor=white" />
 </a>
</p>
<p align="right">
 <a href="buymeacoffee.com/dionpuji120">
   <img src="https://img.shields.io/badge/buy_me_a_coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" />
 </a>
</p>

---

# Connect With Me

<p align="center">

 <a href="https://instagram.com/dionimbus">
   <img src="https://img.shields.io/badge/Instagram-@dionimbus-E4405F?style=for-the-badge&logo=instagram&logoColor=white" />
 </a>

</p>

---

# License

Distributed under the MIT License. See `LICENSE` for more information.
