import json
import os.path
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

def find_element(self, query):
    try:
        return self.driver.find_element_by_css_selector(query)
    except NoSuchElementException:
        return None
        
def wait_for_element(self, query, timeout=10, frequency=0.1):
    wait = WebDriverWait(self.driver, timeout, frequency)
    wait.until(lambda x: self.find_element(query))
        
def get_config(path):
    with open(path) as f:
        return json.load(f)
        
def get_set(path):
    try:
        with open(path, "r") as f:
            return set([l.rstrip("\n") for l in f])
    except IOError as e:
        return set()

def get_script_path(script):
    path = __file__
    path = os.path.abspath(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "js", "{0}.js".format(script))
    return path

def execute_script(self, script, *args):
    with open(get_script_path(script)) as f:
        return self.driver.execute_script(f.read(), *args)

def execute_async_script(self, script, *args):
    with open(get_script_path(script)) as f:
        return self.driver.execute_async_script(f.read(), *args)
