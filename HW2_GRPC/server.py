import grpc
import logs_pb2
import logs_pb2_grpc
import requests
from concurrent import futures

class LogRetrieverService(logs_pb2_grpc.LogRetrieverServicer):
    def GetMessages(self, request, context):
        print("GetMessages request received!")
        endpoint = f"https://qnvqyz4nka.execute-api.us-east-2.amazonaws.com/test/indexes?start={request.start}&delta={request.delta}"
        results = requests.get(endpoint)

        logs_reply = logs_pb2.MessagesReply()
        logs_reply.startIndex = results.json()["startIndex"]
        logs_reply.endIndex = results.json()["endIndex"]
        
        
        return logs_reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    logs_pb2_grpc.add_LogRetrieverServicer_to_server(LogRetrieverService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
