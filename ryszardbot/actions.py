from datetime import datetime
import logging
from time import sleep
from selenium.common.exceptions import TimeoutException
from ryszardbot.helpers import execute_script

def remove_failed_posts(self):
    hour = datetime.now().hour
    if hour < 11 or hour >= 23:
        logging.info("removal of failed posts suspended")
        return
    
    logging.info("removing failed posts")
    self.driver.get("https://www.facebook.com/groups/{0}/?sorting_setting=CHRONOLOGICAL".format(self.group))
    
    posts = self.execute_script("getposts")
    now = datetime.now(tz=None).timestamp()
    
    if len(posts) == 0:
        logging.error("failed to fetch posts")
    
    for post in posts:
        difference = (now - post["time"]) / 3600
        
        if post["admin"]:
            logging.info("post by {0} allowed due to adminship {1}".format(post["author"], post["permalink"]))
            continue
            
        if difference >= 24:
            logging.info("post by {0} grandfathered in ({1:.2f} hours) {2}".format(post["author"], difference, post["permalink"]))
            continue
            
        if difference >= 1 and post["likeCount"] >= 50:
            logging.info("post by {0} passed ({1} likes) {2}".format(post["author"], post["likeCount"], post["permalink"]))
            continue
            
        if difference < 1:
            logging.info("post by {0} isn't old enough ({1:.2f} hours) {2}".format(post["author"], difference, post["permalink"]))
            continue
        
        logging.info("post by {0} marked for deletion ({1} likes in {2:.2f} hours) {3}".format(post["author"], post["likeCount"], difference, post["permalink"]))
        message = "AUTOMATYCZNE USUNIĘCIE: LICZBA REAKCJI {0} PO {1:.2f} GODZ.\n\n"
        message += "Wpisy które nie osiągnęły 50 reakcji w ciągu godziny są automatycznie usuwane. "
        message += "Usuwanie jest zawieszone w godzinach od 23 do 11."
        
        result = self.remove_post(post["permalink"], message.format(post["likeCount"], difference))
        
        if result:
            logging.info("post deleted successfully")
        else:
            logging.error("couldn't remove post")
            bot.driver.save_screenshot("screenshot.png")
            
    self.driver.get("about:blank")

def remove_post(self, permalink, reason):
    return self.execute_script("deletepost", permalink, reason)
