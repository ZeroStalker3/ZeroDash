import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PROXY_URL = os.getenv("PROXY_URL")

MAC_ADDR = "9c:6b:00:bd:30:c7" 
NET_INT = "wlp2s0" 
LOG_PATH = "/home/zeroyz/ZeroDash/bot.log"

