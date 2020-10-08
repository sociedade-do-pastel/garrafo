from abc import ABC, abstractmethod
from errorHandler import *
from datetime import date, time
import os

# if there isn`t a root directory, create one
# raise an exception if that's impossible to do
def checkRoot(root):
    if not os.path.isdir(root):
        os.mkdir(root)

def checkProtocol(protocol_string):
    if protocol_string != "HTTP/1.1":
        raise HTTPnotSupported 


class RequestFactory:
    """Design Pattern Factory para devolver custom requests"""
    @staticmethod
    def makeRequest(message, server_info):
        root_path = "./{}".format(server_info[1])
        try:
            checkRoot(root_path)
            checkProtocol(message.protocol)
            if message.method == "GET":
                return ResponseGet(message, server_info)
            elif message.method == "POST":
                return ResponsePost(messag, server_info)
            elif message.method == "PUT":
                return ResponsePut(message, server_info)
            else:
                raise BadRequest
        except GeneralError as err:
            return ResponseError(message, err, server_info)

class Response(ABC):
    def __init__(self, message, server_info):
        self.hostname  = server_info[1]
        self.system    = server_info[0]
        # Date  = "Date" ":" HTTP-date
        self.date = date.today().strftime("%a, %d %b %Y %H:%M:%S %Z")
        self.response = "HTTP/1.1 {}\n\rServer: {}\n\rContent-Type: {}; charset=utf-8\n\rDate: {}\n\r\n\r{}"
        
    
    @abstractmethod
    def makeResponse(self):
        pass

class ResponseGet(Response):
    def __init__(self, message, server_info):
        super().__init__(message, server_info)
    
    def makeResponse(self):
        pass

class ResponsePost(Response):
    def __init__(self, message, server_info):
        super().__init__(message, server_info)

    def makeResponse(self):
        pass

class ResponsePut(Response):
    def __init__(self, message, server_info):
        super().__init__(message, server_info)

    def makeResponse(self):
        pass

class ResponseError(Response):
    def __init__(self, message, error, server_info):
       super().__init__(message, server_info)
       self.makeResponse(error)

    def makeResponse(self, err):
        self.response = self.response.format(err.error_message, self.hostname, "text/html", self.date, err.error_response)
