from datetime import datetime
import logging
from ryszardbot.helpers import execute_script

def collect_garbage(self):
    # check if garbage collection is enabled at this time
    hour = datetime.now().hour
    if hour < self.config["start_hour"] or hour >= self.config["end_hour"]:
        logging.info("removal of failed posts suspended")
        return
    
    # navigate to group and get posts
    logging.info("scanning for failed posts")
    self.driver.get("https://www.facebook.com/groups/{0}/?sorting_setting=CHRONOLOGICAL".format(self.config["group"]))
    self.wait_for_element("[role=article][id*=post]")
    posts = self.execute_script("getposts")
    
    # if posts failed to fetch, report error
    if len(posts) == 0:
        logging.error("failed to fetch posts")
        self.driver.get("about:blank")
        return
    
    # see if anything changed since last scan
    changes = False
    
    # get post states and handle them accordingly
    for post in posts:
        post_state = get_post_state(post, self.config)
        previous_post_state = self.post_states.get(post["permalink"], "")
        
        # report state changes
        if previous_post_state != post_state or post_state == "pending_removal":
            logging.info(format_state_message(post_state, post))
            self.post_states[post["permalink"]] = post_state
            changes = True
        
        # remove post
        if post_state == "pending_removal":
            result = self.execute_script("deletepost", post["permalink"], format_removal_message(post, self.config))
            
            if result:
                logging.info("post removed successfully")
            else:
                logging.error("couldn't remove post")
                self.driver.save_screenshot("ryszardbot.png")
                
    # report no changes
    if not changes:
        logging.info("no changes since last scan")
    
    # navigate to blank page
    self.driver.get("about:blank")

def get_post_state(post, config):
    age = (datetime.now(tz=None).timestamp() - post["time"]) / 3600
    
    if post["admin"] and config["admins_exempt"]:
        return "exempt_admin"
    if post["moderator"] and config["moderators_exempt"]:
        return "exempt_moderator"
    if age >= config["grandfather_time"]:
        return "grandfathered"
    if age >= config["like_check_time"] and post["likeCount"] >= config["like_count"]:
        return "passed"
    if age < config["like_check_time"]:
        return "maturing"

    return "pending_removal"

def format_state_message(post_state, post):    
    format_string = {
        "exempt_admin": "post by {author} allowed due to adminship",
        "exempt_moderator": "post by {author} allowed due to moderatorship",
        "grandfathered": "post by {author} grandfathered in ({age:.2f} hours)",
        "passed": "post by {author} passed ({like_count} likes)",
        "maturing":  "post by {author} isn't old enough ({age:.2f} hours)",
        "pending_removal": "post by {author} marked for deletion ({like_count} likes in {age:.2f} hours)"
    }[post_state] + " {permalink}"
    
    return format_string.format(author=post["author"],
                                age=(datetime.now(tz=None).timestamp() - post["time"]) / 3600,
                                like_count=post["likeCount"],
                                permalink=post["permalink"])
                                
def format_removal_message(post, config):
    message = "AUTOMATIC REMOVAL: {like_count} REACTIONS AFTER {age:.2f} HOURS\n\n"
    message += "Entries that didn't reach {min_likes} reactions in {min_age} hours are automatically removed. "
    message += "Removal is suspended from {end_time} to {start_time}."
    
    return message.format(like_count=post["likeCount"],
                          age=(datetime.now(tz=None).timestamp() - post["time"]) / 3600,
                          min_likes=config["like_count"],
                          min_age=config["like_check_time"],
                          end_time=config["end_hour"],
                          start_time=config["start_hour"])
