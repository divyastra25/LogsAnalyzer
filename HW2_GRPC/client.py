import grpc
import logs_pb2
import logs_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = logs_pb2_grpc.LogRetrieverStub(channel)

        get_msg_req = logs_pb2.GetMessageReq(start="08:16:46", delta="00:00:24")
        logs_reply = stub.GetMessages(get_msg_req)
        print("GetMessages response receieved!")
        print(logs_reply)

if __name__ == "__main__":
    run()
