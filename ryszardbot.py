import code
import logging
import sys
import time
import traceback
from threading import Thread
import ryszardbot

# configure logging to file
logging.basicConfig(
    handlers=[logging.FileHandler("ryszardbot.log", "a", "utf-8")],
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO)

# also log to stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel("INFO")
stdout_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logging.getLogger().addHandler(stdout_handler)

logging.info("bot starting")
bot = ryszardbot.RyszardBot()
bot.start_driver()

logging.info("logging in")
bot.log_in()

logging.info("bot online")

while True:
    try:
        bot.remove_failed_posts()
    except:
        logging.error(traceback.format_exc())
        
    time.sleep(600)
    

bot.kill_driver()
