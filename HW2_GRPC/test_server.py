import unittest
from http import client
import grpc
import logs_pb2
import logs_pb2_grpc
import logging
from configparser import ConfigParser

logging.basicConfig(filename="logs/client_logs.log", level=logging.NOTSET)

configFile = "config.ini"
config = ConfigParser()
config.read(configFile)

def run(testDate, testStart, testDelta):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = logs_pb2_grpc.LogRetrieverStub(channel)
        logging.info("Client stub created!")
        
        # get_msg_req = logs_pb2.GetMessageReq(date="2022-11-01", start="17:44:33", delta="00:01:02")
        get_msg_req = logs_pb2.GetMessageReq(date=testDate, start=testStart, delta=testDelta)
        logging.info("GetMessageReq Sent!")

        logs_reply = stub.GetMessages(get_msg_req)
        logging.info("GetMessages response receieved!")
        logging.info(logs_reply)
        return logs_reply


class TestClientServerLambda(unittest.TestCase):
    def test_invalid_interval(self):
        date = config['test_client']['date']
        startTime = str(config['test_client']['invalidIntervalStart'])
        deltaTime = str(config['test_client']['invalidIntervalDelta'])
        result = run(date, startTime, deltaTime)

        self.assertEquals(result.message, "Interval not present or No logs in the interval")
        self.assertEquals(result.coded_logs, [])

    def test_invalid_date(self):
        date = config['test_client']['invalidDate']
        startTime = str(config['test_client']['start'])
        deltaTime = str(config['test_client']['delta'])
        result = run(date, startTime, deltaTime)

        self.assertEquals(result.message, "Incorrect Date/Format or No Logs For The Date: 2012-07-01")
        self.assertEquals(result.coded_logs, [])

    def test_invalid_date_format(self):
        date = config['test_client']['invalidDateFormat']
        startTime = str(config['test_client']['start'])
        deltaTime = str(config['test_client']['delta'])
        result = run(date, startTime, deltaTime)

        self.assertEquals(result.message, "Incorrect Date/Format or No Logs For The Date: 02-28-2017")
        self.assertEquals(result.coded_logs, [])

    def test_invalid_time(self):
        date = config['test_client']['date']
        startTime = str(config['test_client']['invalidStartFormat'])
        deltaTime = str(config['test_client']['invalidDeltaFormat'])
        result = run(date, startTime, deltaTime)

        self.assertEquals(result.message, "Time input format incorrect. Enter in HH:MM:SS format.")
        self.assertEquals(result.coded_logs, [])

    def test_valid_input(self):
        date = config['test_client']['date']
        startTime = str(config['test_client']['start'])
        deltaTime = str(config['test_client']['delta'])
        result = run(date, startTime, deltaTime)

        self.assertEquals(result.message, "Logs Found in the Interval.")
        self.assertEquals(len(result.coded_logs), 25)

if __name__ == "__main__":
    unittest.main()
