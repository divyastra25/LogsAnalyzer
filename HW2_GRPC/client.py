from http import client
import grpc
import logs_pb2
import logs_pb2_grpc
import logging
from configparser import ConfigParser

#start logging and set the file to save logs
logging.basicConfig(filename="logs/client_logs.log", level=logging.NOTSET)

#reading program configuration from config.ini file
configFile = "config.ini"
config = ConfigParser()
config.read(configFile)
date = config['client']['date']
startTime = str(config['client']['start'])
deltaTime = str(config['client']['delta'])

def run():
    # connecting to the server
    with grpc.insecure_channel("localhost:50051") as channel:
        # getting the stub through channel
        stub = logs_pb2_grpc.LogRetrieverStub(channel)
        logging.info("Client stub created!")
        
        # Constructing a GetMessageReq with config parameters
        get_msg_req = logs_pb2.GetMessageReq(date=date, start=startTime, delta=deltaTime)
        logging.info("GetMessageReq Sent!")

        # asking the stub to make the RPC call to server
        logs_reply = stub.GetMessages(get_msg_req)
        logging.info("GetMessages response receieved!")
        logging.info(logs_reply)
        print(logs_reply.message)
        print(logs_reply.coded_logs)
        print(len(logs_reply.coded_logs))

if __name__ == "__main__":
    logging.info("Running the client")
    run()
