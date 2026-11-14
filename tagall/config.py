import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

def required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} belum diatur.")
    return value

BOT_TOKEN = required("BOT_TOKEN")
APP_ID = int(required("APP_ID"))
API_HASH = required("API_HASH")
LOGGER_ID = int(required("LOGGER_ID"))
MONGO_DB_URI = required("MONGO_DB_URI")
DB_NAME = os.getenv("DB_NAME", "tagall")
BOT_WORKERS = int(os.getenv("BOT_WORKERS", "4"))
OWNER_NAME = os.getenv("OWNER_NAME", "Owner")
OWNER_ID = [int(x) for x in os.getenv("OWNER_ID", "").replace(",", " ").split()]
CREATOR = OWNER_ID

BROADCAST_AS_COPY = True
PLUG = dict(root="tagall/plugins")

LOG_FILE_NAME = "tagall_logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
