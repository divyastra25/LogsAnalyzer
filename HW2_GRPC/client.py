from http import client
import grpc
import logs_pb2
import logs_pb2_grpc
import logging

logging.basicConfig(filename="logs/client_logs.log", level=logging.NOTSET)
# from configparser import ConfigParser

# configFile = "config.ini"
# config = ConfigParser()
# config.read(configFile)

# startTime = str(config['client']['start'])
# deltaTime = str(config['client']['delta'])

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = logs_pb2_grpc.LogRetrieverStub(channel)
        logging.info("Client stub created!")
        
        get_msg_req = logs_pb2.GetMessageReq(date="2022-11-01", start="01:40:33", delta="00:20:02")
        logging.info("GetMessageReq Sent!")

        logs_reply = stub.GetMessages(get_msg_req)
        logging.info("GetMessages response receieved!")
        logging.info(logs_reply)
        print(logs_reply.message)
        print(len(logs_reply.coded_logs))

if __name__ == "__main__":
    logging.info("Running the client")
    run()
