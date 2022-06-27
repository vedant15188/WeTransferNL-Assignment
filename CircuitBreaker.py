import requests

class CircuitBreaker:
    def __init__(self, http_client, error_threshold, time_window):
        self.http_client = http_client
        self.error_threshold = error_threshold
        self.time_window = time_window
        self.errorCount = 0

    def do_request(self, url):
        #go nuts!
        pass

if __name__ == "__main__":
    print("Hello WeTransfer!!\n-------------------------------\n")

    timeOut = int(input("Input the timeout threshold (in seconds): "))
    errThreshold = int(input("Input the error threshold: "))

    N = int(input("Enter the total number of requests you want to send: "))

    breaker = CircuitBreaker(requests, errThreshold, timeOut)

    for i in range(N):
        print("Request no. ", i+1)
        # do stuff breaker.do_request
