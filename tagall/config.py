import os
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7227138679:AAF5w9tl3pWeOu3YnJjtcoVRRdTKK2VGhjU")
BOT_WORKERS = int(os.environ.get("BOT_WORKERS", "4"))

APP_ID = int(os.environ.get("APP_ID", "22016511"))
API_HASH = os.environ.get("API_HASH", "8267335b1cbd700a179dbe9a9a482d1e")

LOGGER_ID = int(os.environ.get("LOGGER_ID", "-1002109872719"))

MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://Aanjink:memek@cluster0.qv2th.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "yeflfny899")
BROADCAST_AS_COPY = True

PLUG = dict(root="tagall/plugins")

OWNER_ID = [int(x) for x in (os.environ.get("OWNER_ID", "728409811").split())]
OWNER_NAME = os.environ.get("OWNER_NAME", "@viinotpii")


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

CREATOR = [ 728409811
]
