from datetime import datetime
import logging
from time import sleep
from selenium.common.exceptions import TimeoutException
from ryszardbot.helpers import execute_script

def remove_failed_posts(self):
    hour = datetime.now().hour
    if hour < 9 or hour >= 23:
        logging.info("removal of failed posts suspended")
        return
    
    logging.info("scanning for failed posts")
    self.driver.get("https://www.facebook.com/groups/{0}/?sorting_setting=CHRONOLOGICAL".format(self.group))
    
    posts = self.execute_script("getposts")
    now = datetime.now(tz=None).timestamp()
    changes = False
    
    if len(posts) == 0:
        logging.error("failed to fetch posts")
        self.driver.get("about:blank")
        return
    
    for post in posts:
        post_state = None
        post_state_message = None
        difference = (now - post["time"]) / 3600
        
        if post["admin"]:
            post_state = "exempt_admin"
            post_state_message = "post by {0} allowed due to adminship {1}".format(post["author"], post["permalink"])
        elif difference >= 24:
            post_state = "grandfathered"
            post_state_message = "post by {0} grandfathered in ({1:.2f} hours) {2}".format(post["author"], difference, post["permalink"])
        elif difference >= 1 and post["likeCount"] >= 50:
            post_state = "passed"
            post_state_message = "post by {0} passed ({1} likes) {2}".format(post["author"], post["likeCount"], post["permalink"])
        elif difference < 1:
            post_state = "maturing"
            post_state_message = "post by {0} isn't old enough ({1:.2f} hours) {2}".format(post["author"], difference, post["permalink"])
        else:
            post_state = "pending_removal"
            post_state_message = "post by {0} marked for deletion ({1} likes in {2:.2f} hours) {3}".format(post["author"], post["likeCount"], difference, post["permalink"])
        
        if self.post_states.get(post["permalink"], "") != post_state or post_state == "pending_removal":
            logging.info(post_state_message)
            self.post_states[post["permalink"]] = post_state
            changes = True
        
        if post_state == "pending_removal":
            message = "AUTOMATYCZNE USUNIĘCIE: LICZBA REAKCJI {0} PO {1:.2f} GODZ.\n\n"
            message += "Wpisy które nie osiągnęły 50 reakcji w ciągu godziny są automatycznie usuwane. "
            message += "Usuwanie jest zawieszone w godzinach od 23 do 9."
            
            result = self.remove_post(post["permalink"], message.format(post["likeCount"], difference))
            
            if result:
                logging.info("post removed successfully")
            else:
                logging.error("couldn't remove post")
                self.driver.save_screenshot("ryszardbot.png")
            
    if not changes:
        logging.info("no changes since last scan")
            
    self.driver.get("about:blank")

def remove_post(self, permalink, reason):
    return self.execute_script("deletepost", permalink, reason)
