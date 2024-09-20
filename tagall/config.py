import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7339072581:AAH55NxPUswhnixiWE6zLAnOdqyHd2f7EeU")
BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))

APP_ID = int(os.environ.get("APP_ID", "22016511"))
API_HASH = os.environ.get("API_HASH", "8267335b1cbd700a179dbe9a9a482d1e")

LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1002063460821"))

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "yeflfny899")
BROADCAST_AS_COPY = True

PLUG = dict(root="tagall/plugins")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "6953052196").split())]
OWNER_NAME = os.environ.get("OWNER_NAME", "@Darenrorr")


LOG_FILE_NAME = "antigcast_logs.txt"
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

CREATOR = [ 7043537972
]
