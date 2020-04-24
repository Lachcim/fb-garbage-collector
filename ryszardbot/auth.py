from ryszardbot.helpers import get_credentials

def log_in(self, username=None, password=None, credentials_path="credentials.json"):
    # get credentials from file if needed
    if not username or not password:
        credentials = get_credentials(credentials_path)
        username = credentials["username"]
        password = credentials["password"]

    # type username and password into login form and submit
    self.wait_for_element("#email")
    self.find_element("#email").click()
    self.find_element("#email").send_keys(username)
    self.find_element("#pass").click()
    self.find_element("#pass").send_keys(password)
    self.find_element("[data-testid=royal_login_button]").click()
    
    # wait until the main application has loaded
    self.wait_for_element("#userNav")
