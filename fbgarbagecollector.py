import logging
import platform
import sys
import time
import traceback
import fbgc

# configure logger
logging.basicConfig(
    handlers=[
        logging.FileHandler("fbgarbagecollector.log", "a", "utf-8"),
        logging.StreamHandler(sys.stdout)
    ],
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO)

# create virtual display for Chrome on Unix
if platform.system() != "Windows":
    from pyvirtualdisplay import Display
    Display(visible=False, size=(800, 600)).start()

# create instance of the bot
bot = fbgc.FBGarbageCollector()
logged_in = False

try:
    logging.info("bot starting")
    
    # get configuration and log in
    bot.get_config()
    bot.start_driver()
    bot.log_in()
    
    # enable main loop on success
    logged_in = True
except KeyboardInterrupt:
    # skip main loop
    pass
except:
    # log error, skip main loop
    logging.error(traceback.format_exc())
    bot.take_screenshot()
    
# do main loop if logged in
while logged_in:
    try:
        bot.collect_garbage()
        time.sleep(bot.config["collect_interval"])
    except KeyboardInterrupt:
        # stop main loop on keyboard interrupt
        break
    except:
        # log error
        logging.error(traceback.format_exc())
        bot.take_screenshot()
    
# exit gracefully
logging.info("bot shutting down")
bot.kill_driver()
