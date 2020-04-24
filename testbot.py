import code
import traceback
from threading import Thread
import ryszardbot

bot = ryszardbot.RyszardBot()
bot.start_driver()
bot.log_in()

def console_exit():
    raise SystemExit

try:
    code.interact(local={"exit": console_exit, "bot": bot})
except SystemExit:
    pass
    
pull_events = False
bot.kill_driver()
