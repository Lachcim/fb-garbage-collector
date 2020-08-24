import logging
import os.path
import psutil
from selenium import webdriver
from fbgc.helpers import get_config, get_set

class FBGarbageCollector:  
    def __init__(self):
        self.driver = None
        self.credentials = None
        self.config = None
        self.post_states = {}
        self.deleted_posts = set()
        
    def start_driver(self):
        # create Chrome headless driver
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("log-level=3")
        options.add_argument("user-agent=Mozilla/5.0 Chrome/80.0 FBGarbageCollector/1.0")
        options.add_argument("user-data-dir={}".format(os.path.abspath("userdata")))
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(chrome_options=options)
        
    def kill_driver(self):
        # give the driver a chance to quit on peaceful terms
        if self.driver:
            try:
                self.driver.quit()
            except KeyboardInterrupt:
                # catch keyboard interrupt and move on to forceful killing
                pass
        
        # ensure there are no zombie processes
        # repeat procedure until successful
        while True:
            try:
                # iterate over process list
                forceful = False
                for process in psutil.process_iter():            
                    try:
                        # look for chrome processes with the webdriver signature
                        if process.name() not in ["chrome.exe", "chromium"]:
                            continue
                        if not "--test-type=webdriver" in process.cmdline():
                            continue
                        
                        # mark killing procedure as forceful
                        if not forceful:
                            logging.info("forcefully killing chrome processes")
                            forceful = True
                        
                        # kill zombie process
                        process.kill()
                    except psutil.NoSuchProcess:
                        # handle already killed processes
                        pass
                
                # break loop on success
                break
            except KeyboardInterrupt:
                # catch keyboard interrupt to ensure the procedure is complete before quitting
                pass
                
        logging.info("driver killed")
            
    def get_config(self):
        self.credentials = get_config("credentials.json")
        self.config = get_config("config.json")
        self.deleted_posts = get_set("deletedposts.txt")
    
    from fbgc.auth import log_in
    from fbgc.garbage import collect_garbage
    from fbgc.misc import post
    from fbgc.helpers import (find_element,
                              wait_for_element,
                              execute_script,
                              execute_async_script,
                              take_screenshot)
