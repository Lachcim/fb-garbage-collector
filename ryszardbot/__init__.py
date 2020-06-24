import os.path
from selenium import webdriver

class RyszardBot:  
    def __init__(self):
        self.driver = None
        self.post_states = {}
        
    def start_driver(self):
        # create Chrome headless driver
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("log-level=3")
        options.add_argument("user-agent=Mozilla/5.0 Chrome/80.0 RyszardBot/0.1")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(chrome_options=options)
        
    def kill_driver(self):
        if self.driver:
            try:
                # ignore exceptions due to Python shutting down
                self.driver.quit()
            except:
                pass
    
    from ryszardbot.auth import log_in
    from ryszardbot.garbage import collect_garbage
    from ryszardbot.helpers import (find_element,
                                    wait_for_element,
                                    execute_script,
                                    execute_async_script)
