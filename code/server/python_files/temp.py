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
converted_today = datetime.strptime(date1, "%b %d, %Y")


def login(usernameArg, passwordArg):
    # print(driver.current_url)
    time.sleep(5)
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
    time.sleep(5)


def expand_shadow_element(element):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", element)
    return shadow_root


def filterCourses(shadow_root):
    # print("Navigating to Semesters...")
    filterRoot1 = shadow_root.find_element_by_css_selector("d2l-tabs")
    filter_shadow_root1 = expand_shadow_element(filterRoot1)
    filterRoot2 = filter_shadow_root1.find_elements_by_css_selector("d2l-tab-internal")

    # print("Navigating to current semester...")
    filters = []
    for i in filterRoot2:
        filters.append(i)
    filter1 = filters[
        2
    ]  # Navigates to current semester (2 -- Current Sem, 3 -- Previous Sem, 0 -- All Courses)
    panelID = filter1.get_attribute("controls-panel")
    filter1.click()

    # print("Reached current semester...")
    return panelID


def getClasses(shadow_root, panelID):
    # print("Navigating to class_urls...")
    tabRoot1 = shadow_root.find_element_by_id(panelID)
    root3 = tabRoot1.find_element_by_css_selector("d2l-my-courses-content")
    shadow_root3 = expand_shadow_element(root3)
    root4 = shadow_root3.find_element_by_css_selector("d2l-my-courses-card-grid")
    shadow_root4 = expand_shadow_element(root4)
    root5 = shadow_root4.find_elements_by_css_selector("d2l-enrollment-card")

    # print("Obtaining class information...")
    class_urls = []
    class_names = []
    for i in root5:
        shadow_root5 = expand_shadow_element(i)
        class1 = shadow_root5.find_element_by_css_selector("d2l-card")
        class_urls.append(class1.get_attribute("href"))
        class_names.append(class1.text.split(":")[0])  # Gets only the course name

    # print("Obtained class information...")
    return class_urls, class_names


def getAssignmentDueDates(due_date_elements):
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
                assignment_folder_elements[i].find_element_by_tag_name("a").text
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


def getAssignmentInformation(class_names, class_urls):
    item_type = "Assignments"
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
    assignment_due_dates = getAssignmentDueDates(due_date_elements)
    assignment_json = jsonify(
        assignment_names,
        assignment_completion_status,
        assignment_due_dates,
        class_names,
        class_urls,
        item_type,
    )

    return assignment_json


def getQuizInformation(class_names, class_urls):
    item_type = "Quizzes"
    quiz_table = driver.find_element_by_tag_name("table")

    completion_status_class = "//td[@class='d_gn']"
    quiz_folder_class = "//a[@title='Quiz summary']"
    due_date_class = "//div[@class='drt d2l-htmlblock d2l-htmlblock-untrusted d2l-htmlblock-deferred']"

    quiz_folder_elements = quiz_table.find_elements_by_xpath(quiz_folder_class)
    completion_status_elements = quiz_table.find_elements_by_xpath(
        completion_status_class
    )
    due_date_elements = quiz_table.find_elements_by_xpath(due_date_class)

    quiz_names = getQuizFolderNames(quiz_folder_elements)
    quiz_completion_status = getQuizCompletionStatus(completion_status_elements)
    quiz_due_dates = getQuizDueDates(due_date_elements)
    quiz_json = jsonify(
        quiz_names,
        quiz_completion_status,
        quiz_due_dates,
        class_names,
        class_urls,
        item_type,
    )

    return quiz_json


def getQuizFolderNames(quiz_folder_elements):
    quiz_names_array = []
    for i in range(len(quiz_folder_elements)):
        quiz_name = quiz_folder_elements[i].text
        quiz_names_array.append(quiz_name)
    return quiz_names_array


def getQuizDueDates(due_date_class):
    date_array = []
    for i in range(0, len(due_date_class)):
        quiz_date_temp = due_date_class[i].text
        if quiz_date_temp.split(" ")[0] == "Available":
            quiz_date = quiz_date_temp[13:25].strip()
        elif quiz_date_temp.split(" ")[0] == "Due":
            quiz_date = quiz_date_temp[7:19].strip()
        else:
            quiz_date = None
        date_array.append(quiz_date)
    return date_array


def getQuizCompletionStatus(completion_status_elements):
    completion_status_array = []
    for i in range(len(completion_status_elements)):
        completion_status = completion_status_elements[i].text
        if completion_status == " ":
            completion_status = None
        completion_status_array.append(completion_status)
    return completion_status_array


def filterAssignmentInformation(assignment_data):
    assignment_names = assignment_data["itemObject"].get("itemNames")
    assignment_completion_statuses = assignment_data["itemObject"].get(
        "itemCompletionStatuses"
    )
    assignment_dates = assignment_data["itemObject"].get("itemDueDates")
    assignment_names_filtered = []
    assignment_completion_statuses_filtered = []
    assignment_dates_filtered = []

    for i in range(len(assignment_names)):
        date = assignment_dates[i]
        if date != None:
            converted_date = datetime.strptime(date, "%b %d, %Y %I:%M %p")
            if (converted_date >= converted_today) and (
                assignment_completion_statuses[i] == "Not Submitted"
            ):
                assignment_dates_filtered.append(date[0:12])
                assignment_names_filtered.append(assignment_names[i])
                assignment_completion_statuses_filtered.append(
                    assignment_completion_statuses[i]
                )
        else:
            if assignment_completion_statuses[i] == "Not Submitted":
                assignment_dates_filtered.append(date)
                assignment_names_filtered.append(assignment_names[i])
                assignment_completion_statuses_filtered.append(
                    assignment_completion_statuses[i]
                )

    assignment_data_filtered = jsonify(
        assignment_names_filtered,
        assignment_completion_statuses_filtered,
        assignment_dates_filtered,
        assignment_data["class_names"],
        assignment_data["class_urls"],
        assignment_data["itemType"],
    )
    return assignment_data_filtered


def filterQuizInformation(quiz_data):
    quiz_names = quiz_data["itemObject"].get("itemNames")
    quiz_completion_statuses = quiz_data["itemObject"].get("itemCompletionStatuses")
    quiz_dates = quiz_data["itemObject"].get("itemDueDates")
    quiz_names_filtered = []
    quiz_completion_statuses_filtered = []
    quiz_dates_filtered = []

    for i in range(len(quiz_names)):
        date = quiz_dates[i]
        if date != None:
            converted_date = datetime.strptime(date, "%b %d, %Y")
            if (converted_date >= converted_today) and (
                quiz_completion_statuses[i] == None
            ):
                quiz_dates_filtered.append(date)
                quiz_names_filtered.append(quiz_names[i])
                quiz_completion_statuses_filtered.append(quiz_completion_statuses[i])
        else:
            if quiz_completion_statuses[i] == None:
                quiz_dates_filtered.append(date)
                quiz_names_filtered.append(quiz_names[i])
                quiz_completion_statuses_filtered.append(quiz_completion_statuses[i])

    quiz_data_filtered = jsonify(
        quiz_names_filtered,
        quiz_completion_statuses_filtered,
        quiz_dates_filtered,
        quiz_data["class_names"],
        quiz_data["class_urls"],
        quiz_data["itemType"],
    )

    return quiz_data_filtered


def TodoItem(item_name, item_due_date, item_completion_status):
    return {
        "_id": "",
        "_listId": "",
        "title": item_name,
        "description": "",
        "creationDate": "",
        "dueDate": item_due_date,
        "isComplete": item_completion_status,
    }


def TodoList(class_name, todo_items):
    return {
        "_id": "",
        "title": class_name,
        "description": "",
        "creationDate": "",
        "todoItemsCollection": todo_items,
    }


def jsonify(
    item_names,
    item_completion_statuses,
    item_due_dates,
    class_names,
    class_urls,
    item_type,
):
    return {
        "class_names": class_names,
        "class_urls": class_urls,
        "itemType": item_type,
        "itemObject": {
            "itemNames": item_names,
            "itemCompletionStatuses": item_completion_statuses,
            "itemDueDates": item_due_dates,
        },
    }


def createTodoItems(data):
    item_names = data["itemObject"].get("itemNames")
    item_due_dates = data["itemObject"].get("itemDueDates")
    todo_items = []
    for i in range(len(item_names)):
        todo_item = TodoItem(item_names[i], item_due_dates[i], False)
        todo_items.append(todo_item)
    return todo_items


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
    time.sleep(5)

    class_urls, class_names = getClasses(shadow_root2, panelID)

    user_data = {
        "user": {"username": username, "password": password},
        "data": {"TodoList": []},
    }

    data = []

    for i in range(len(class_urls)):
        uniqueClassID = class_urls[i][10:16]
        assignmentURL = (
            "https://avenue.cllmcmaster.ca/d2l/lms/dropbox/user/folders_list.d2l?ou="
            + uniqueClassID
            + "&isprv=0"
        )

        driver.get(assignmentURL)

        # print(f"Obtaining assignment information for {class_names[i]}...")

        todo_list = TodoList(class_names[i], [])
        assignment_data = getAssignmentInformation(class_names[i], class_urls[i])
        assignment_data_filtered = filterAssignmentInformation(assignment_data)
        todo_items_assignments = createTodoItems(assignment_data_filtered)
        todo_list = TodoList(class_names[i], todo_items_assignments)
        data.append(todo_list)
        # print(f"Retrieved all assignment information for {class_names[i]}...")

    for i in range(len(class_urls)):
        uniqueClassID = class_urls[i][10:16]
        quizURL = (
            "https://avenue.cllmcmaster.ca/d2l/lms/quizzing/user/quizzes_list.d2l?ou="
            + uniqueClassID
        )

        driver.get(quizURL)

        # print(f"Obtaining quiz information for {class_names[i]}...")

        quiz_data = getQuizInformation(class_names[i], class_urls[i])
        quiz_data_filtered = filterQuizInformation(quiz_data)
        todo_items_quizzes = createTodoItems(quiz_data_filtered)
        if data[i]["title"] == class_names[i]:
            data[i]["todoItemsCollection"].extend(todo_items_quizzes)
        user_data["data"]["TodoList"].append(data[i])
        # print(f"Retrieved all quiz information for {class_names[i]}...")

    with open("data.json", "w") as outfile:
        json.dump(user_data, outfile)


if __name__ == "__main__":
    main()