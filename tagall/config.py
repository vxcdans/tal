import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "9141890878:AAECYNgnCEJCK1sCqDDAZSau4yzSK9vQ-Fw")
BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))

APP_ID = int(os.environ.get("APP_ID", "29346197"))
API_HASH = os.environ.get("API_HASH", "4de265464017f7a1342946f8a32d1a59")

LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1004338630617)

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://germsnstus_db_user:JEVAGBlM9QjCdnI2@cluster0.6ccczyf.mongodb.net/EvoBot?retryWrites=true&w=majority&authSource=admin")
DB_NAME = os.environ.get("DB_NAME", "germsnstus_db_user)
BROADCAST_AS_COPY = True

PLUG = dict(root="tagall/plugins")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "8033557981").split())]
OWNER_NAME = os.environ.get("OWNER_NAME", "@fvckdans")


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

CREATOR = [ 8033557981
]
