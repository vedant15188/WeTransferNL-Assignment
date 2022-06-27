import requests
from time import sleep
import threading
from http.server import HTTPServer

import Server

def startServer(webServer):
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

class CircuitBreaker:
    def __init__(self, http_client, error_threshold, time_window):
        self.http_client = http_client
        self.error_threshold = error_threshold
        self.time_window = time_window
        self.errorCount = 0

    def do_request(self, url):
        try:
            response = self.http_client.get(url)
            print(response)
            if(response.status_code == 200):
                print("Successful response!")
                self.errorCount = 0
            else:
                print("Not a successful request!")
                raise Exception()
        except:
            self.errorCount += 1
            print("error count: ", self.errorCount)
            if(self.errorCount >= self.error_threshold):
                print("Circuit Open!")
                print("Circuit is currenty in open state so no new requests to the service will be entertained!")
                print("sleeping for ", self.time_window, " secs")
                sleep(self.time_window)
                self.errorCount = 0

if __name__ == "__main__":
    print("Hello WeTransfer!!\n-------------------------------\n")

    try:
        webServer = HTTPServer(("localhost", 8000), Server.MyServer)
        print("Starting simple python HTTP server...")

        # Starting the HTTP Server on a new thread to keep the main prog. running
        serverThread = threading.Thread(target=startServer, args=(webServer,))
        serverThread.daemon = True
        serverThread.start()

        print("Server started http://%s:%s" % ("localhost", 8000))

        timeOut = int(input("Input the timeout threshold (in seconds): "))
        errThreshold = int(input("Input the error threshold: "))

        N = int(input("Enter the total number of requests you want to send: "))

        breaker = CircuitBreaker(requests, errThreshold, timeOut)

        for i in range(N):
            print("Request no. ", i+1)
            # Condition to simulate OPEN condition for CircuitBreaker
            if((i % (errThreshold*2)) < errThreshold):
                print("Simulating error")
                breaker.do_request("http://localhost:8000/error")
            else:
                print("Simulating normal request")
                breaker.do_request("http://localhost:8000/")
            sleep(1)
    except Exception as e:
        print(e)
        print("Failed to start the server")
        quit()