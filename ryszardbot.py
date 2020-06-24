import code
import logging
import sys
import time
import traceback
from threading import Thread
from pyvirtualdisplay import Display
import ryszardbot

# configure logging to file
logfile_handler = logging.FileHandler("ryszardbot.log", "a", "utf-8")
logfile_handler.setLevel("INFO")
logfile_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logging.getLogger().addHandler(logfile_handler)

# also log to stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel("INFO")
stdout_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logging.getLogger().addHandler(stdout_handler)

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
