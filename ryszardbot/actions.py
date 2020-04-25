from datetime import datetime
from time import sleep
from selenium.common.exceptions import TimeoutException
from ryszardbot.helpers import execute_script

def remove_failed_posts(self):
    self.driver.get("https://www.facebook.com/groups/{0}/?sorting_setting=CHRONOLOGICAL".format(self.group))
    
    posts = self.execute_script("getposts")
    now = datetime.now(tz=None).timestamp()
    
    for post in posts:
        if post["admin"]:
            print("post by {0} allowed due to adminship".format(post["author"]))
            continue
            
        if now - post["time"] >= 86400:
            print("post by {0} grandfathered in".format(post["author"]))
            continue
            
        if now - post["time"] >= 3600 and post["likeCount"] >= 50:
            print("post by {0} passed".format(post["author"]))
            continue
            
        if now - post["time"] < 3600:
            print("post by {0} isn't old enough ({1:.2f} hours)".format(post["author"], (now - post["time"]) / 3600))
            continue
            
        message = "AUTOMATYCZNE USUNIĘCIE: LICZBA REAKCJI {0} PO {1:.2f} GODZ.\n\n"
        message += "Aby utrzymać wysoki poziom grupy, wpisy które nie osiągnęły 50 reakcji w ciągu godziny są automatycznie usuwane. "
        message += "Usuwanie jest zawieszone w godzinach od 23 do 11."
            
        print("post by {0} marked for deletion, {1} likes reached in {2:.2f} hours".format(post["author"], post["likeCount"], (now - post["time"]) / 3600))
        result = self.remove_post(post["permalink"], message.format(post["likeCount"], (now - post["time"]) / 3600))
        
        if result:
            print("post deleted successfully")
        else:
            print("couldn't remove post")

def remove_post(self, permalink, reason):
    return self.execute_script("deletepost", permalink, reason)
