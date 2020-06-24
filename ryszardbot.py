import code
import logging
import platform
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
if platform.system() != "Windows":
    Display(visible=False, size=(800, 600)).start()

# start bot and log in
logging.info("bot starting")
bot = ryszardbot.RyszardBot()
bot.get_config()
bot.start_driver()
bot.log_in()

while True:
    try:
        bot.collect_garbage()
    except:
        logging.error(traceback.format_exc())
        bot.driver.save_screenshot("screenshot.png")
        
    time.sleep(bot.config["collect_interval"])
    

bot.kill_driver()
