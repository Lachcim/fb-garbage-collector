import os.path
from selenium import webdriver

class RyszardBot:  
    def __init__(self):
        self.driver = None
        self.group = None
        
    def start_driver(self, driver=None, downloads="downloads"):
        # provide default driver
        if not driver:
            options = webdriver.ChromeOptions()
            # options.add_argument("headless")
            options.add_argument("log-level=3")
            options.add_argument("user-agent=Mozilla/5.0 Chrome/80.0 RyszardBot/0.1")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            prefs = {
                "profile.default_content_settings.popups": 0,
                "profile.default_content_setting_values.automatic_downloads": 1,
                "download.default_directory": os.path.abspath(downloads)
            }
            options.add_experimental_option("prefs", prefs)
            
            driver = webdriver.Chrome(chrome_options=options)
        
        # start: request login screen
        self.driver = driver
        self.driver.get("https://www.facebook.com/")
        
    def kill_driver(self):
        if self.driver:
            try:
                # ignore exceptions due to Python shutting down
                self.driver.quit()
            except:
                pass
    
    from ryszardbot.actions import remove_failed_posts
    from ryszardbot.auth import log_in
    from ryszardbot.helpers import (find_element,
                                    wait_for_element,
                                    execute_script,
                                    execute_async_script)
