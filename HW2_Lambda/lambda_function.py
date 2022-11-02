import json
# import boto3
from datetime import datetime, timedelta
import os
import hashlib
import re

# binary search returns the index of logs after or before a timestamp depending on
# if it is start timestand of end timestamp
def binarySearchTime(logs, time, isStart):
    low = 0
    high = len(logs) - 1
    mid = 0

    # Have used a while loop because AWS Lambda has limited memory and using recursion would create a
    # new array of logs on stack frame at each recursive call, which would be inefficient in terms of space.
    while low <= high:
        mid = (low + high) // 2
        currLogTime = datetime.strptime(logs[mid].split()[0], "%H:%M:%S.%f")

        if currLogTime < time:
            low = mid+1
        elif currLogTime > time:
            high = mid-1
        else:
            return mid

    return low if isStart else high

def lambda_handler(event, context):
    # construct the log file name based on date queryParameter
    date = event["queryStringParameters"]["date"]
    logFilename = f"LogFileGenerator.{date}.log"
    
    results = {}
    
    try:
        # try opening and reading the log file
        f = open(f"/mnt/logs/LogFileGenerator/log/{logFilename}", "r")
        log_list = f.readlines()
    except IOError:
        # log file could not be opened meaning it does not exist
        print(f"Incorrect Date/Format or No Logs For The Date: {date}")
        results["message"] = f"Incorrect Date/Format or No Logs For The Date: {date}"
        results["logs_coded"] = []
        
        response = {}
        response["statusCode"] = 400
        response["headers"] = {}
        response["headers"]["Content-Type"] = "application/json"
        response["body"] = json.dumps(results)
        return response
        
    try:
        startTime = datetime.strptime(event["queryStringParameters"]["start"], "%H:%M:%S")
        deltaTime = datetime.strptime(event["queryStringParameters"]["delta"], "%H:%M:%S")
    except:
        # Parameter timestamps are not in the correct format
        print("Time input format incorrect. Enter in HH:MM:SS format.")
        results["message"] = "Time input format incorrect. Enter in HH:MM:SS format."
        results["logs_coded"] = []
        
        response = {}
        response["statusCode"] = 400
        response["headers"] = {}
        response["headers"]["Content-Type"] = "application/json"
        response["body"] = json.dumps(results)
        return response

    delta = timedelta(hours=deltaTime.hour, minutes=deltaTime.minute, seconds=deltaTime.second)
    endTime = startTime + delta;
    
    startIndex = binarySearchTime(log_list, startTime, True)
    endIndex = binarySearchTime(log_list, endTime, False)
    
    if startIndex <= endIndex:
        # logs found between the interval, check if they contain the regex pattern and return them
        messages_list = []
        idx = startIndex
        while (idx <= endIndex):
            log_message = log_list[idx].split()[4]
            match = re.search("([a-c][e-g][0-3]|[A-Z][5-9][f-w]){5,15}", log_message)
            if match is not None:
                messages_list.append(hashlib.md5(log_message.encode()).hexdigest())
            idx += 1

        results["message"] = "Logs Found in the Interval."
        results["logs_coded"] = messages_list
    
        # #construct http response
        response = {}
        response["statusCode"] = 200
        response["headers"] = {}
        response["headers"]["Content-Type"] = "application/json"
        response["body"] = json.dumps(results)

        return response
    else:
        # No logs found within the interval
        print("Interval not present or No logs in the interval")
        results["message"] = "Interval not present or No logs in the interval"
        results["logs_coded"] = []
        
        #construct http response
        response = {}
        response["statusCode"] = 400
        response["headers"] = {}
        response["headers"]["Content-Type"] = "application/json"
        response["body"] = json.dumps(results)
        

        return response
