# Steam Gift Trade Accepter 🤖

A bot for automatically accepting gift trades in Steam. Checks for new trade offers at set intervals and automatically accepts suitable ones.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features
- Automatic gift trade acceptance
- Operation logging
- Storage of accepted items history in database
- Configurable check interval
- Steam Guard (.maFile) support

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/steam-gift-trade-accepter.git
cd steam-gift-trade-accepter
```

2. Install dependencies:
```bash
python -m venv .venv
source venv/bin/activate # Linux
source venv/scripts/activate # Windows
pip install -r requirements.txt
```
3. Create .env file based on .env.example
Fill in all required parameters

## 🔧 Configuration
```ini
TIME_OUT = "10"  # Trade check interval (in seconds)
DATABASE_URL = "sqlite:///gift_trades.db"  # Database path
TABLE_NAME = "cs2_received_items"  # Table name for item storage
LOG_FILE_NAME = "steam_gift_accepter.log"  # Log filename
LOG_FILE_PATH = ""  # Log path (if empty - current directory)

STEAM_API_KEY = 'your_api_key'  # Steam API key
STEAMGUARD_PATH = 'path/to/steamguard/123.maFile'  # Steam Guard file path
STEAM_USERNAME = 'your_login'  # Steam username
STEAM_PASSWORD = 'your_password'  # Steam password
```

## 🏃 Running
```bash
python main.py
```

📊 Database (Table structure for CS2 items)
- item_id - Item ID
- classid - Class ID
- instanceid - Instance ID
- amount - Quantity of identical items
- market_hash_name - Item name
- received_at - Receiving time

⚠️ Important
Do not publish your .env file!
Use a separate Steam account for the bot
Steam may restrict accounts for automation
