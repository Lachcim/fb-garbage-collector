import code
import logging
import sys
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

def console_exit():
    raise SystemExit

try:
    code.interact(local={"exit": console_exit, "bot": bot})
except SystemExit:
    pass
    
pull_events = False
bot.kill_driver()
