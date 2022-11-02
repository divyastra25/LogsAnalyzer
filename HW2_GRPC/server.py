import grpc
import logs_pb2
import logs_pb2_grpc
import requests
from concurrent import futures
import logging

#start logging and set the file to save logs
logging.basicConfig(filename="logs/server_logs.log", level=logging.NOTSET)

class LogRetrieverService(logs_pb2_grpc.LogRetrieverServicer):
    def GetMessages(self, request, context):
        print("GetMessages request received!")
        logging.info("GetMessages request received!")
        # constructing the endpoint URL with queryParameters
        endpoint = f"https://qggew40x1g.execute-api.us-east-2.amazonaws.com/demo/logs?date={request.date}&start={request.start}&delta={request.delta}"
        results = requests.get(endpoint)  #making a http get request and waiting for results
        print("results received")
        logging.info("Results Received!")
        print(results.json()["message"])

        # constructing the MessageReply to be returned
        logs_reply = logs_pb2.MessagesReply()
        logs_reply.message = results.json()["message"]
        logs_reply.coded_logs.extend(results.json()["logs_coded"])
        
        logging.info("Sending Reply")
        return logs_reply

def serve():
    # defining the server with 5 max clients
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))

    # adding the class and server to the Servicer
    logs_pb2_grpc.add_LogRetrieverServicer_to_server(LogRetrieverService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()  # starting server
    logging.info("Server Started!")
    server.wait_for_termination()  # keeing the server alive

if __name__ == "__main__":
    logging.info("Starting serve()")
    serve()
