import code
import logging
import sys
import time
import traceback
from threading import Thread
from pyvirtualdisplay import Display
import ryszardbot

# configure logger
logging.basicConfig(
    handlers=[
        logging.FileHandler("ryszardbot.log", "a", "utf-8"),
        logging.StreamHandler(sys.stdout)
    ],
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO)

# create virtual display for Chrome
display = Display(visible=False, size=(800, 600)).start()

# start bot and log in
logging.info("bot starting")
bot = ryszardbot.RyszardBot()
bot.start_driver()
logging.info("logging in")
bot.log_in()
logging.info("bot online")

while True:
    try:
        bot.collect_garbage()
    except:
        logging.error(traceback.format_exc())
        bot.driver.save_screenshot("screenshot.png")
        
    time.sleep(600)
    

bot.kill_driver()
