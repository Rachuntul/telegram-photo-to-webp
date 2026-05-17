<div align="center">
  <h1>Telegram Premium Multi-Converter Bot</h1>
  <p>A powerful, lightweight, and Docker-optimized Telegram bot for image processing and document generation.</p>

  [![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Telegram API](https://img.shields.io/badge/Telegram_Bot_API-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

  <br />

  [Features](#key-features) •
  [Installation](#quick-start-guide) •
  [Usage](#usage) •
  [Support & Donate](#support--donate) •
  [Contact](#connect-with-me)
</div>

---

## Key Features

*Click on each feature to expand details:*

<details>
<summary><b>Format Conversion</b></summary>
<br>
Convert images seamlessly to WebP (auto-compressed <100KB), PNG, and JPG while maintaining visual quality. Ideal for web optimization.
</details>

<details>
<summary><b>Document Generation</b></summary>
<br>
Convert images directly to PDF, Word (DOCX), and Excel (XLSX) utilizing LibreOffice headless mode operating natively within the Docker container.
</details>

<details>
<summary><b>Aesthetic Filters</b></summary>
<br>
Apply professional color grading such as Fujifilm Chrome, Teal & Orange, Leica Monochrome, Cyberpunk Neon, Pencil Sketch, and Vintage Sepia via matrix manipulation.
</details>

<details>
<summary><b>Upscaling Resolution</b></summary>
<br>
Upscale image resolution up to 2x using advanced Lanczos resampling for crisp details without pixelation.
</details>

<details>
<summary><b>RAM Disk Optimization</b></summary>
<br>
Leverages Docker `tmpfs` to process files directly in memory. Bypasses slow disk I/O bottlenecks entirely, ensuring instant processing even on slower external storage.
</details>

## Tech Stack

* **Core**: Python 3.11
* **API Framework**: `python-telegram-bot`
* **Image Processing**: Pillow (PIL), NumPy
* **Document Engine**: LibreOffice (Headless)
* **Deployment**: Docker & Docker Compose

---

## Quick Start Guide

### 1. Clone the Repository
```bash
git clone [github.com/Rachuntul/telegram-photo-to-webp.git](https://github.com/Rachuntul/telegram-photo-to-webp.git)
cd telegram-photo-to-webp
```

### 2. Configuration

Create your environment variable file by copying the example:
```Bash
cp .env.example .env
```

Edit .env and assign your bot token from @BotFather:
Plaintext
```Bash
BOT_TOKEN=your_telegram_bot_token_here
```

### 3. Launch via Docker

This project is configured to run inside an isolated Docker container with a RAM Disk setup for maximum performance.
```Bash
docker compose up -d --build
```

Usage

    Start a chat with your bot on Telegram.

    Send an image using the Photo attachment option.

    The bot will present an interactive inline menu.

    Select your preferred format, document type, filter, or upscale action.

    The processed file will be returned instantly as an uncompressed document.

Support & Donate

If you find this project helpful and want to support, you can support me through the link below:
Connect with Me
License

Distributed under the MIT License. See LICENSE for more information.
