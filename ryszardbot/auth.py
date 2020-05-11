from ryszardbot.helpers import get_credentials

def log_in(self, username=None, password=None, credentials_path="credentials.json"):
    # get credentials from file if needed
    if not username or not password:
        credentials = get_credentials(credentials_path)
        username = credentials["username"]
        password = credentials["password"]
        self.group = credentials["group"]

    # type username and password into login form and submit
    self.wait_for_element("#email")
    self.find_element("#email").click()
    self.find_element("#email").send_keys(username)
    self.find_element("#pass").click()
    self.find_element("#pass").send_keys(password)
    self.find_element("[data-testid=royal_login_button]").click()
    
    # wait until the main application has loaded or the code prompt appears
    self.wait_for_element("#userNav, #approvals_code")
    
    # handle code prompt
    codeInput = self.find_element("#approvals_code")
    if codeInput:
        # prompt for and type code
        code = input("Authentication code: ")
        codeInput.click()
        codeInput.send_keys(code)
        
        # submit code and don't save device
        self.find_element("#checkpointSubmitButton").click()
        self.wait_for_element("input[value=dont_save]")
        self.find_element("input[value=dont_save]").click()
        self.find_element("#checkpointSubmitButton").click()
        
        # wait for the main app or the unknown device dialog
        self.wait_for_element("#userNav, #checkpointSecondaryButton")
        
        # click through unknown device dialog
        if self.find_element("#checkpointSecondaryButton"):
            self.find_element("#checkpointSubmitButton").click()
            self.wait_for_element("input[value=dont_save]")
            self.find_element("input[value=dont_save]").click()
            
            self.wait_for_element("#userNav, #")

    # navigate to blank page
    self.driver.get("about:blank")
