import os
import csv
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
# telebot
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()
# any configuration should be stored here

TOKEN = os.getenv("TOKEN")  # configure env if you need;
API_ID = os.getenv("API_ID")  # Input your api_id here
API_HASH = os.getenv("API_HASH")  # Input your api_hash here

DEBUG = False
SERVER_URL = os.getenv("SERVER_URL")

SESSION = os.getenv("SESSION")

fieldnames = ["First Name", "Last Name", "Username", "Id", "User Status"]


# Connection of all the integrated APIs
loop = asyncio.new_event_loop()
client = TelegramClient(StringSession(SESSION), api_id=API_ID,
                        api_hash=API_HASH, loop=loop).start()
