# Logs Finder: AWS Lambda with AkkaHTTP & gRPC

### Name: Divya Patel
### Link to Video: https://youtu.be/1HRtp3jZ_Z4

## Overview:
This is an implementation of a Log Finder/Analyzer using AWS Lambda and AWS Elastic File System. AWS EFS is mounted on an EC2 Instance that continuously produces logs and stores them in EFS. AWS Lambda houses the code for analyzing the logs and access the same logs produced by EC2 using EFS. The analysis to be done is to find logs within the time interval and see if they match a regex pattern, those than do should be returned as a md-5 generated hash code.

## Implementation:
**Lambda:** The logs are produced on a daily basis. The lambda function takes in date, start timestamp and delta timestamp as query string parameters. Based on the date the log file is loaded and read. Then binary search is performed to find the start and end indexes for the logs within the time interval. Then, based on the logs appropriate response with a message is constructed and returned. The lambda function is exposed to AWS API Gateway so that it can be triggered using REST API.

*Note:* The binary search uses a while loop because lambda memory is limited and using recursion will cause it to reproduce the logs array in each stack frame of the recursive call. Thus, recursion is not effient in terms of memory of the lambda.

**AkkaHTTP:** AkkaHTTP is a toolkit for consuming HTTP-based services in Scala and Java. The HTTP_Client is a Scala sub-project in the repo which uses the AkkaHTTP module to make RESTful calls to the AWS API Gateway which triggers the lambda function.

**gRPC:** gRPC is a high performance RPC framework that can be implemented in many lanaguages. The HW2_GRPC sub-project is a python project that implements gRPC. It has a client that makes a rpc call to the server with input parameters and then the server calls makes a HTTP request to the AWS API Gateway which triggers the lambda and returns a response, the gRPC server then returns that response back to gRPC client. The communication between the gRPC server and client is done through protocol buffers, which is a very effient and fast way to (de)serialize data.

## Execution:
**Lambda:** Firstly, attach EFS to the log producing code so that logs can be stored in EFS.
Then, create the lambda function with access to the same EFS. Add AWS API Gateway requests as a trigger to the lambda function.

**AkkaHTTP:** Make sure to have Java and SBT installed on your machine. Natigate to the HTTP_Client sub-project of the repo. Adjust the configurations in the application.conf file in src/main/resources/. Then, run the following commands to compile and run the project, which prints the results of the query/log analysis:
```
sbt clean compile
```
```
sbt run
```


**gRPC:** 
Navigate to the HW2_GRPC sub-project of the repo.

pip install the grpcio-tools with the following command:
```
pip3 install grpcio-tools
```
Then run the following command to compile the proto file to produce some auto generated code:
```
python3 -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/logs.proto
```
Then make the appropriate configurations in the config.ini file under [client] section.
Run the following commands to start the server and client.
```
python3 server.py
```
```
python3 client.py
```
After running the client it should output the results with the appropriate response from the lambda.