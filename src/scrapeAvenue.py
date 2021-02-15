from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from requests import get
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

load_dotenv()
avenueWebsiteURL = 'https://cap.mcmaster.ca/mcauth/login.jsp?app_id=1505&app_name=Avenue'


service = Service('chromedriver.exe')
service.start()
chrome_options = Options();
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(avenueWebsiteURL)
print(driver.current_url)
time.sleep(5);
username = driver.find_element_by_name('user_id')
password = driver.find_element_by_name('pin')
submit = driver.find_element_by_name("submit")
username.clear()
password.clear()
username.send_keys(os.getenv("macid"))
password.send_keys(os.getenv("pass"))
submit.click()
time.sleep(5)

avenue_homepage_url = driver.current_url
avenue_homepage_html = requests.get(avenue_homepage_url).content

def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

root1 = driver.find_element_by_tag_name('d2l-my-courses')
shadow_root1 = expand_shadow_element(root1)

root2 = shadow_root1.find_element_by_tag_name('d2l-my-courses-container')
shadow_root2 = expand_shadow_element(root2)

root3 = shadow_root2.find_element_by_css_selector('d2l-my-courses-content')
shadow_root3 = expand_shadow_element(root3)

root4 = shadow_root3.find_element_by_css_selector('d2l-my-courses-card-grid')
shadow_root4 = expand_shadow_element(root4)

root5 = shadow_root4.find_element_by_css_selector('d2l-enrollment-card')
shadow_root5 = expand_shadow_element(root5)

class1 = shadow_root5.find_element_by_css_selector('d2l-card')
print(class1.get_attribute('href'))
