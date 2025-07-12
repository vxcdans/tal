import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))

APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

LOGGER_ID = int(os.environ.get("LOGGER_ID", ""))

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "")
BROADCAST_AS_COPY = True

PLUG = dict(root="tagall/plugins")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "6735026878").split())]
OWNER_NAME = os.environ.get("OWNER_NAME", "@eldanskuy")


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

CREATOR = [ 6735026878
]
