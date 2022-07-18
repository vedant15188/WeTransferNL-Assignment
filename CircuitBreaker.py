import requests
from time import sleep
from datetime import datetime
import threading
from http.server import HTTPServer
from queue import Queue

# Import custom HTTP server module
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
        self.errorQueue = Queue(maxsize=error_threshold)
        # Circuit state, 0 for closed, 1 for open
        self.state = 0

    def do_request(self, url):
        try:
            response = self.http_client.get(url)
            print(response)

            if(self.errorQueue.full()):
                self.state = 1
                print("Circuit Open!!")
                print("Circuit is currenty in open state so no new requests to the service will be entertained!\n\n")
                raise Exception()
            elif(response.status_code == 200):
                print("Successful response!")
                self.errorQueue = Queue(maxsize=self.error_threshold)
            else:
                print("Not a successful request!")
                raise Exception()
        except:
            errorEvent = {
                "errorCode": response.status_code,
                "timeStamp": datetime.now()
            }

            # Insert the error event if the queue is empty
            if(self.errorQueue.empty()):
                self.errorQueue.put(errorEvent)
            # Exit the function if the circuit is open!
            elif(self.state == 1):
                self.errorQueue = Queue(maxsize=self.error_threshold)
                return
            else:
                queueCondition = True

                # Keep dequeuing the error events till we're within the confines of the time window and then insert the event.
                # errorQueue.queue[0] will get the first element of the queue without removing it
                while(queueCondition):
                    if(int((errorEvent["timeStamp"] - self.errorQueue.queue[0]["timeStamp"]).total_seconds()) > self.time_window):
                        self.errorQueue.get()
                    else:
                        queueCondition = False
                        self.errorQueue.put(errorEvent)

            print("error count: ", self.errorQueue.qsize())

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

        timeWindow = int(input("Input the time window (in seconds): "))
        errThreshold = int(input("Input the error threshold: "))

        N = int(input("Enter the total number of requests you want to send: "))

        breaker = CircuitBreaker(requests, errThreshold, timeWindow)

        # Sending N requests at every second
        for i in range(N):         
            print("Request no. ", i+1)
            
            # Condition to simulate OPEN condition for CircuitBreaker
            if((i % (errThreshold*2)) < errThreshold):
                print("Simulating error")
                breaker.do_request("http://localhost:8000/error")
            else:
                print("Simulating normal request")
                breaker.do_request("http://localhost:8000/")

            if(breaker.state == 1):
                print("sleeping for ", timeWindow, " secs")
                sleep(timeWindow)
                breaker.state = 0
            
            sleep(1)
    except Exception as e:
        print(e)
        quit()