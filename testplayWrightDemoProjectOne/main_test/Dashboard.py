import logging
import os
import requests
import json
import base64
from datetime import datetime




AWS_IP = "https://app.11automation.com/"
Project_API_Key = "66437375abbc352004eee7a0"
global Login_Token
screenshot =[]

def Eleven_Automation_Login():
    print("Entered into Eleven_Automation_Login method....")
    url = AWS_IP + "api/v1/auth/login"

    payload = json.dumps(
        {"email": "*******", "password": "*****"}
    )
    headers = {"Content-Type": "application/json", "Authorization": "Basic Og=="}

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False
    )

    if str(response.status_code) == "200":
        resp_data = response.json()
        print(resp_data.get("token"))
        Login_Token = resp_data.get("token")
    else:
        Login_Token = None

    print("Exiting from  Eleven_Automation_Login method....")
    return Login_Token


def Eleven_Automation_Iteration(RT_Login_Token):
    print("Entered into Eleven_Automation_Iteration method....")
    url = AWS_IP + "api/v1/iterations/" + Project_API_Key
    # payload = json.dumps(dict(Iteration_data),default=str)
    print(url)

    payload = json.dumps(
        {
            "iterationId": "Testing",
            "testType": "Automation",
            "browserUsed": "Chrome",
            "browserVersion": "122",
            "executionStartTime": str(datetime.now()),
            "executionEndTime": str(datetime.now()),
        },
        default=str,
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + str(RT_Login_Token),
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)

    if str(response.status_code) == "201" or str(response.status_code) == "200":
        resp_data = response.json()
        print(resp_data["_id"])
        Iteration_Id = resp_data["_id"]
    else:
        Iteration_Id = None

    print("Exiting from Eleven_Automation_Iteration method....")
    return Iteration_Id


def Eleven_Automation_TestCase(RT_Login_Token, RT_Iteration_Id, Dashboard_list):
    url = AWS_IP + "api/v1/testcases/" + RT_Iteration_Id
    logging.debug(Dashboard_list)
    testcase_list = []
    i = 0
    while i < len(Dashboard_list):
        if Dashboard_list[i][2] == "Pass":
            element = {
                "testCaseId": Dashboard_list[i][0],
                "testCaseSummary": Dashboard_list[i][1],
                "result": Dashboard_list[i][2],
                "executionTime": Dashboard_list[i][3],
            }
            i += 1
            testcase_list.append(element)
        else:
            element = {
                "testCaseId": Dashboard_list[i][0],
                "testCaseSummary": Dashboard_list[i][1],
                "result": Dashboard_list[i][2],
                "executionTime": Dashboard_list[i][3],
                "failureTrace": Dashboard_list[i][4],
                "screenshot": Dashboard_list[i][5],
            }
            i += 1
            testcase_list.append(element)
            
    payload = json.dumps(testcase_list)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + RT_Login_Token,
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def image_to_base64(dashboardList):
    image_path = os.getcwd() + "\\screenshots\\main_test"
    for imgage in os.listdir(image_path):
        with open(image_path+"\\"+imgage, "rb") as img_file:
            # Read the image file
            img_data = img_file.read()
            # Encode the image data to base64
            base64_string = base64.b64encode(img_data).decode('utf-8')
            for sublist in dashboardList:
            # Check if the third element of the sublist matches st
                if sublist[1] in imgage:
                    # Append st to the sublist
                    sublist.append(base64_string)
                    break
    return dashboardList


def dashboard_main(Dashboard_list):
    if any("Fail" in x  for x in Dashboard_list):
        Dashboard_list = image_to_base64(Dashboard_list)
    RT_Login_Token = Eleven_Automation_Login()
    RT_Iteration_Id = Eleven_Automation_Iteration(
        RT_Login_Token,
    )
    Eleven_Automation_TestCase(RT_Login_Token, RT_Iteration_Id, Dashboard_list)   
