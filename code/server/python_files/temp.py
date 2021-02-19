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
import platform
import json
import sys

load_dotenv()
avenueWebsiteURL = (
    "https://cap.mcmaster.ca/mcauth/login.jsp?app_id=1505&app_name=Avenue"
)

service = Service(
    "chromedriver" if platform.system() == "Darwin" else "chromedriver.exe"
)
service.start()
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
today = date.today()
date1 = today.strftime("%b %d, %Y")
d1 = datetime.strptime(date1, "%b %d, %Y")


def login(usernameArg, passwordArg):
    # print(driver.current_url)
    time.sleep(4)
    username = driver.find_element_by_name("user_id")
    password = driver.find_element_by_name("pin")
    submit = driver.find_element_by_name("submit")

    # print("Clearing Username and Password...")
    username.clear()
    password.clear()

    # print("Entering Username and Password...")
    username.send_keys(usernameArg)
    password.send_keys(passwordArg)

    # print("Submitting Username and Password...")
    submit.click()

    # print("Waiting for login...")
    time.sleep(4)


def expand_shadow_element(element):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", element)
    return shadow_root


def filterCourses(shadow_root):
    # Rename filters to semesters and teach jash how to name variabels
    # print("Navigating to Semesters...")
    filterRoot1 = shadow_root.find_element_by_css_selector("d2l-tabs")
    filter_shadow_root1 = expand_shadow_element(filterRoot1)
    filterRoot2 = filter_shadow_root1.find_elements_by_css_selector("d2l-tab-internal")

    # print("Navigating to current semester...")
    filters = []
    for i in filterRoot2:
        filters.append(i)
    filter1 = filters[2]  # Navigates to current semester
    panelID = filter1.get_attribute("controls-panel")
    filter1.click()

    # print("Reached current semester...")
    return panelID


def getClasses(shadow_root, panelID):
    # Change classes --> class_urls
    # Change classNames --> class_names
    # print("Navigating to classes...")
    tabRoot1 = shadow_root.find_element_by_id(panelID)
    root3 = tabRoot1.find_element_by_css_selector("d2l-my-courses-content")
    shadow_root3 = expand_shadow_element(root3)
    root4 = shadow_root3.find_element_by_css_selector("d2l-my-courses-card-grid")
    shadow_root4 = expand_shadow_element(root4)
    root5 = shadow_root4.find_elements_by_css_selector("d2l-enrollment-card")

    # print("Obtaining class information...")
    classes = []
    classNames = []
    for i in root5:
        shadow_root5 = expand_shadow_element(i)
        class1 = shadow_root5.find_element_by_css_selector("d2l-card")
        classes.append(class1.get_attribute("href"))
        classNames.append(class1.text.split(":")[0])  # Gets only the course name

    # print("Obtained class information...")
    return classes, classNames


def getAssignmentDueDate(due_date_elements):
    date_array = []
    for i in range(len(due_date_elements)):
        try:
            date_label = due_date_elements[i].find_element_by_css_selector("label").text
            date_array.append(date_label)
        except:
            date_array.append(None)
    return date_array


def getAssignmentCompletionStatus(completion_status_elements):
    completion_status_array = []
    for i in range(len(completion_status_elements)):
        try:
            completion_status = completion_status_elements[i].find_element_by_tag_name(
                "a"
            )
            completion_status_array.append(completion_status.text)
        except NoSuchElementException:
            try:
                completion_status = completion_status_elements[
                    i
                ].find_element_by_css_selector("label")
                completion_status_array.append(completion_status.text)
            except:
                completion_status_array.append(None)
    return completion_status_array


def getAssignmentFolderNames(assignment_folder_elements):
    assignment_names_array = []
    for i in range(len(assignment_folder_elements)):
        try:
            assignment_name = (
                assignment_folder_elements[i]
                .find_element_by_tag_name("a")
                .get_attribute("title")
            )
            assignment_names_array.append(assignment_name)
        except NoSuchElementException:
            try:
                assignment_name = (
                    assignment_folder_elements[i].find_element_by_tag_name("label").text
                )
                assignment_names_array.append(assignment_name)
            except:
                assignment_names_array.append(None)

    return assignment_names_array


def jsonify(assignment_names, completion_statuses, due_dates, class_names, class_urls):
    return {
        "class_names": class_names,
        "class_urls": class_urls,
        "assignmentObject": {
            "assignmentNames": assignment_names,
            "assignmentCompletionStatuses": completion_statuses,
            "assignmentDueDates": due_dates,
        },
    }


def getAssignmentInformation(class_names, class_urls):
    assignment_table = driver.find_element_by_tag_name("table")

    completion_status_class = "//td[@class='d_gn d_gc d_gt']"
    assignment_folder_class = ".dco.d2l-foldername"
    due_date_class = "td.d_gn.d_gc.d_gt.d2l-table-cell-last"

    assignment_folder_elements = assignment_table.find_elements_by_css_selector(
        assignment_folder_class
    )
    completion_status_elements = assignment_table.find_elements_by_xpath(
        completion_status_class
    )
    due_date_elements = assignment_table.find_elements_by_css_selector(due_date_class)

    assignment_names = getAssignmentFolderNames(assignment_folder_elements)
    assignment_completion_status = getAssignmentCompletionStatus(
        completion_status_elements
    )
    assignment_due_dates = getAssignmentDueDate(due_date_elements)
    assignment_json = jsonify(
        assignment_names,
        assignment_completion_status,
        assignment_due_dates,
        class_names,
        class_urls,
    )

    return assignment_json


# def getQuizSubmissions():
#     tableRoot1 = driver.find_element_by_tag_name("table")
#     tableRoot2 = tableRoot1.find_elements_by_xpath("//td[@class='d_gn']")
#     submissions = []
#     for i in tableRoot2:
#         submission = i.text
#         submissions.append(submission)
#     return submissions


# def getQuizNames():
#     tableRoot1 = driver.find_element_by_tag_name("table")
#     tableRoot2 = tableRoot1.find_elements_by_xpath("//a[@title='Quiz summary']")
#     quizNames = []
#     dates = getQuizDates()
#     for i in range(0, len(tableRoot2)):
#         if dates:
#             d2 = datetime.strptime(dates[i], "%b %d, %Y")
#             if d2 >= d1:
#                 quizName = tableRoot2[i].text
#                 quizNames.append(quizName)
#     return quizNames


# def getQuizDates():
#     tableRoot1 = driver.find_element_by_tag_name("table")
#     tableRoot2 = tableRoot1.find_elements_by_xpath(
#         "//div[@class='drt d2l-htmlblock d2l-htmlblock-untrusted d2l-htmlblock-deferred']"
#     )
#     quizDates = []
#     submissions = getQuizSubmissions()
#     for i in range(0, len(tableRoot2)):
#         quizDate = tableRoot2[i].text
#         quizDate1 = " "
#         d2 = datetime.today()
#         if quizDate.split(" ")[0] == "Available":
#             quizDate1 = quizDate[13:25].strip()
#             d2 = datetime.strptime(quizDate1, "%b %d, %Y")
#         if quizDate.split(" ")[0] == "Due":
#             quizDate1 = quizDate[7:19].strip()
#             d2 = datetime.strptime(quizDate1, "%b %d, %Y")
#         if (d2 >= d1) and submissions[i] != "Feedback: On Attempt":
#             quizDates.append(quizDate1)
#     return quizDates


def main():
    username = sys.argv[1]
    password = sys.argv[2]

    driver.get(avenueWebsiteURL)
    login(username, password)

    root1 = driver.find_element_by_tag_name("d2l-my-courses")
    shadow_root1 = expand_shadow_element(root1)
    root2 = shadow_root1.find_element_by_tag_name("d2l-my-courses-container")
    shadow_root2 = expand_shadow_element(root2)
    panelID = filterCourses(shadow_root2)
    time.sleep(4)

    class_urls, class_names = getClasses(shadow_root2, panelID)

    user_data = {
        "user": {"username": username, "password": password},
        "assignmentObjectArray": [],
        "quizObjectArray": [],
    }

    for i in range(len(class_urls)):
        uniqueClassID = class_urls[i][10:16]
        assignmentURL = (
            "https://avenue.cllmcmaster.ca/d2l/lms/dropbox/user/folders_list.d2l?ou="
            + uniqueClassID
            + "&isprv=0"
        )

        driver.get(assignmentURL)

        # print(f"Obtaining assignment information for {class_names[i]}...")

        assignment_data = getAssignmentInformation(class_names[i], class_urls[i])
        user_data["assignmentObjectArray"].append(assignment_data)
        # print(f"Retrieved all assignment information for {class_names[i]}...")

        # for i in range(len(class_urls)):
        #     uniqueClassID = class_urls[i][10:16]
        #     quizzesURL = (
        #         "https://avenue.cllmcmaster.ca/d2l/lms/quizzing/user/quizzes_list.d2l?ou="
        #         + uniqueClassID
        #     )

        #     driver.get(quizzesURL)

        # print(f"Obtaining quiz information for {class_names[i]}...")
        #     quizNames = getQuizNames()
        #     quizDates = getQuizDates()
        # print(f"Quiz Names for {class_names[i]}: {quizNames}")
        # print(f"Quiz Dates for {class_names[i]}: {quizDates}")
        # print(f"Obtained quiz information for {class_names[i]}...")

    print(json.dumps(user_data))
    with open("data.json", "w") as outfile:
        json.dump(user_data, outfile)


if __name__ == "__main__":
    main()
