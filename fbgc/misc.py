import logging
from fbgc.helpers import find_element, wait_for_element

def post(self, text=None, image=None):
    # navigate to group
    logging.info("creating a post")
    self.driver.get("https://mbasic.facebook.com/groups/{0}/".format(self.config["group"]))
    self.wait_for_element("textarea[name=xc_message]")
    
    # write post body
    if text:
        self.find_element("textarea[name=xc_message]").send_keys(text)
    
    # attach post image
    if image:
        self.find_element("input[name=view_photo]").click()
        self.wait_for_element("input[name=file1]")
        self.find_element("input[name=file1]").send_keys(image)
        self.find_element("input[name=filter_type][value='-1']").click()
        self.find_element("input[name=add_photo_done]").click()
    
    # submit form
    self.find_element("input[name=view_post]").click()
    
    # navigate to blank page when done
    self.wait_for_element("textarea[name=xc_message]")
    logging.info("post created")
    self.driver.get("about:blank")
