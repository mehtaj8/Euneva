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
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from datetime import datetime

load_dotenv()
avenueWebsiteURL = (
    "https://cap.mcmaster.ca/mcauth/login.jsp?app_id=1505&app_name=Avenue"
)

service = Service("chromedriver.exe")
service.start()
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
today = date.today()
date1 = today.strftime("%b %d, %Y")
d1 = datetime.strptime(date1, "%b %d, %Y")

def login():
    print(driver.current_url)
    time.sleep(5)
    username = driver.find_element_by_name("user_id")
    password = driver.find_element_by_name("pin")
    submit = driver.find_element_by_name("submit")
    username.clear()
    password.clear()
    username.send_keys(os.getenv("macid"))
    password.send_keys(os.getenv("pass"))
    submit.click()
    time.sleep(5)


def expand_shadow_element(element):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", element)
    return shadow_root


def filterCourses(shadow_root):
    filterRoot1 = shadow_root.find_element_by_css_selector("d2l-tabs")
    filter_shadow_root1 = expand_shadow_element(filterRoot1)

    filterRoot2 = filter_shadow_root1.find_elements_by_css_selector("d2l-tab-internal")
    filters = []
    for i in filterRoot2:
        filters.append(i)
    filter1 = filters[3]
    panelID = filter1.get_attribute("controls-panel")
    filter1.click()
    return panelID


def getClasses(shadow_root, panelID):
    tabRoot1 = shadow_root.find_element_by_id(panelID)

    root3 = tabRoot1.find_element_by_css_selector("d2l-my-courses-content")
    shadow_root3 = expand_shadow_element(root3)

    root4 = shadow_root3.find_element_by_css_selector("d2l-my-courses-card-grid")
    shadow_root4 = expand_shadow_element(root4)

    root5 = shadow_root4.find_elements_by_css_selector("d2l-enrollment-card")
    classes = []
    classNames = []
    for i in root5:
        shadow_root5 = expand_shadow_element(i)
        class1 = shadow_root5.find_element_by_css_selector("d2l-card")
        classes.append(class1.get_attribute("href"))
        classNames.append(class1.text.split(", ")[1])

    return classes, classNames

def getAssignmentSubmissions():
    tableRoot1 = driver.find_element_by_tag_name("table")
    tableRoot2 = tableRoot1.find_elements_by_xpath("//td[@class='d_gn d_gc d_gt']")
    submissions = []
    for i in tableRoot2:
        try:
            submission = i.find_element_by_css_selector("a")
        except:
            submission = i.find_element_by_css_selector("label")
        submissions.append(submission.text)
    return submissions


def getAssignmentNames():
    tableRoot1 = driver.find_element_by_tag_name("table")
    tableRoot2 = tableRoot1.find_elements_by_css_selector(".dco.d2l-foldername")
    assignmentNames = []
    dates = getAssignmentDates()
    submissions = getAssignmentSubmissions()
    for i in range(0, len(tableRoot2)):
        if dates:
            d2 = datetime.strptime(dates[i], "%b %d, %Y")
            try:
                assignmentName = tableRoot2[i].find_element_by_css_selector("a")
            except NoSuchElementException:
                assignmentName = tableRoot2[i].find_element_by_css_selector("label")
            if submissions[i] == "Not Submitted" and (d2 >= d1):
                assignmentNames.append(assignmentName.text)
    return assignmentNames


def getAssignmentDates():
    tableRoot1 = driver.find_element_by_tag_name("table")
    dateRoot1 = tableRoot1.find_elements_by_css_selector(
        "td.d_gn.d_gc.d_gt.d2l-table-cell-last"
    )
    submissions = getAssignmentSubmissions()
    dates = []
    for i in range(0, len(dateRoot1)):
        try:
            date = dateRoot1[i].find_element_by_css_selector("label")
            date1 = date.text
            d2 = datetime.strptime(date1, '%b %d, %Y %I:%M %p')
            if(submissions[i] == "Not Submitted") and (d2 >= d1):
                dates.append(date1)
        except NoSuchElementException:
            if(submissions[i] == "Not Submitted"):
                dates.append(0)
    return dates

def getQuizSubmissions():
    tableRoot1 = driver.find_element_by_tag_name("table")
    tableRoot2 = tableRoot1.find_elements_by_xpath("//td[@class='d_gn']")
    submissions = []
    for i in tableRoot2:
        submission = i.text
        submissions.append(submission)
    return submissions

def getQuizNames():
    tableRoot1 = driver.find_element_by_tag_name("table")
    tableRoot2 = tableRoot1.find_elements_by_xpath("//a[@title='Quiz summary']")
    quizNames = []
    dates = getQuizDates()
    for i in range(0, len(tableRoot2)):
        if dates:
            d2 = datetime.strptime(dates[i], "%b %d, %Y")
            if(d2 >= d1):
                quizName = tableRoot2[i].text
                quizNames.append(quizName)
    return quizNames


def getQuizDates():
    tableRoot1 = driver.find_element_by_tag_name("table")
    tableRoot2 = tableRoot1.find_elements_by_xpath("//div[@class='drt d2l-htmlblock d2l-htmlblock-untrusted d2l-htmlblock-deferred']")
    quizDates = []
    submissions = getQuizSubmissions()
    for i in range(0, len(tableRoot2)):
        quizDate = tableRoot2[i].text
        quizDate1 = " "
        d2 = datetime.today()
        if(quizDate.split(" ")[0] == "Available"):
            quizDate1 = quizDate[13:25].strip()
            d2 = datetime.strptime(quizDate1, "%b %d, %Y")
        if(quizDate.split(" ")[0] == "Due"):
            quizDate1 = quizDate[7:19].strip()
            d2 = datetime.strptime(quizDate1, "%b %d, %Y")
        if(d2 >= d1) and submissions[i] != "Feedback: On Attempt":
            quizDates.append(quizDate1)
    return quizDates


def main():
    driver.get(avenueWebsiteURL)
    login()

    avenue_homepage_url = driver.current_url
    avenue_homepage_html = requests.get(avenue_homepage_url).content
    root1 = driver.find_element_by_tag_name("d2l-my-courses")
    shadow_root1 = expand_shadow_element(root1)

    root2 = shadow_root1.find_element_by_tag_name("d2l-my-courses-container")
    shadow_root2 = expand_shadow_element(root2)

    panelID = filterCourses(shadow_root2)
    time.sleep(5)

    classes, classNames = getClasses(shadow_root2, panelID)

    for i in classes:
        uniqueClassID = i[10:16]
        assignmentURL = (
            "https://avenue.cllmcmaster.ca/d2l/lms/dropbox/user/folders_list.d2l?ou="
            + uniqueClassID
            + "&isprv=0"
        )

        driver.get(assignmentURL)

        assignmentNames = getAssignmentNames()
        assignmentDates = getAssignmentDates()
        #print(assignmentNames)
        #print(assignmentDates)

    for i in classes:
        uniqueClassID = i[10:16]
        quizzesURL = (
            "https://avenue.cllmcmaster.ca/d2l/lms/quizzing/user/quizzes_list.d2l?ou="
            + uniqueClassID
        )

        driver.get(quizzesURL)

        quizNames = getQuizNames()
        quizDates = getQuizDates()
        print(quizNames)
        print(quizDates)

if __name__ == "__main__":
    main()
