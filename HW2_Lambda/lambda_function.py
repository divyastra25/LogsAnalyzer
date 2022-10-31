import json
# import boto3
from datetime import datetime, timedelta
import os
import hashlib
import re

def binarySearchTime(logs, time, isStart):
    low = 0
    high = len(logs) - 1
    mid = 0

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
    date = event["queryStringParameters"]["date"]
    logFilename = f"LogFileGenerator.{date}.log"
    
    results = {}
    
    try:
        f = open(f"/mnt/logs/{logFilename}", "r")
        log_list = f.readlines()
    except IOError:
        print(f"Incorrect Date/Format or No Logs For The Date: {sys.argv[1]}")
        results["message"] = f"Incorrect Date/Format or No Logs For The Date: {sys.argv[1]}"
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
        
        messages_list = []
        idx = startIndex
        while (idx <= endIndex):
            log_message = log_list[idx].split()[5]
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
