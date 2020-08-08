import os.path
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
        options.add_argument("user-data-dir=userdata")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(chrome_options=options)
        
    def kill_driver(self):
        if self.driver:
            try:
                # ignore exceptions due to Python shutting down
                self.driver.quit()
            except:
                pass
                
    def get_config(self):
        self.credentials = get_config("credentials.json")
        self.config = get_config("config.json")
        self.deleted_posts = get_set("deletedposts.txt")
    
    from fbgc.auth import log_in
    from fbgc.garbage import collect_garbage
    from fbgc.helpers import (find_element,
                              wait_for_element,
                              execute_script,
                              execute_async_script)
