from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
avenueWebsiteURL = 'https://cap.mcmaster.ca/mcauth/login.jsp?app_id=1505&app_name=Avenue'

driver = webdriver.Chrome()
driver.get(avenueWebsiteURL)
print(driver.current_url)
username = driver.find_element_by_name('user_id')
password = driver.find_element_by_name('pin')
submit = driver.find_element_by_name("submit")
username.clear()
password.clear()
username.send_keys(os.getenv("username"))
password.send_keys(os.getenv("password"))
submit.click()
time.sleep(5)

avenue_homepage_url = driver.current_url
avenue_homepage_html = requests.get(avenue_homepage_url).content
print(avenue_homepage_html)
soup = BeautifulSoup(avenue_homepage_html, "html.parser")
print(soup)

classes = soup.findAll("div", "d2l-card-link-text d2l-offscreen")
print(classes)
