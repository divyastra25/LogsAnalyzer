import sys
from datetime import datetime, timedelta
# import boto3

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

f = open("10entriesALL.log", "r")

startTime = datetime.strptime(sys.argv[1], "%H:%M:%S")
deltaTime = datetime.strptime(sys.argv[2], "%H:%M:%S")
delta = timedelta(hours=deltaTime.hour, minutes=deltaTime.minute, seconds=deltaTime.second)
endTime = startTime + delta;

logArr = f.readlines()

print(binarySearchTime(logArr, startTime, True))
print(binarySearchTime(logArr, endTime, False))
