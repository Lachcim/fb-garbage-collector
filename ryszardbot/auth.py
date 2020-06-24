import logging

def log_in(self):
    # navigate to login screen
    self.driver.get("https://www.facebook.com/")
    self.wait_for_element("#email, div[role=navigation]")

    # return if already logged in
    if self.find_element("div[role=navigation]"):
        logging.info("already logged in")
        self.driver.get("about:blank")
        return
        
    logging.info("logging in")
        
    # type username and password into login form and submit
    self.find_element("#email").click()
    self.find_element("#email").send_keys(self.credentials["username"])
    self.find_element("#pass").click()
    self.find_element("#pass").send_keys(self.credentials["password"])
    self.find_element("[data-testid=royal_login_button]").click()
    
    # wait until the main application has loaded or the code prompt appears
    self.wait_for_element("#userNav, #approvals_code")
    
    # handle code prompt
    codeInput = self.find_element("#approvals_code")
    if codeInput:
        logging.info("two factor authentication enabled")
        
        # prompt for and type code
        code = input("Authentication code: ")
        logging.info("authentication code received")
        codeInput.click()
        codeInput.send_keys(code)
        
        # submit code and don't save device
        self.find_element("#checkpointSubmitButton").click()
        self.wait_for_element("input[value=save_device]")
        self.find_element("input[value=save_device]").click()
        self.find_element("#checkpointSubmitButton").click()
        
        # wait for the main app or the unknown device dialog
        self.wait_for_element("#userNav, #checkpointSecondaryButton")
        
        # click through unknown device dialog
        if self.find_element("#checkpointSecondaryButton"):
            logging.info("dismissing unknown device dialog")
            
            self.find_element("#checkpointSubmitButton").click()
            self.wait_for_element("input[value=save_device]")
            self.find_element("input[value=save_device]").click()
            
            self.wait_for_element("#userNav")

    # navigate to blank page
    logging.info("logged in")
    self.driver.get("about:blank")
