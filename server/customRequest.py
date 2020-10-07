from abc import ABC, abstractmethod
from errorHandler import Error
from datetime import date, time

import os

class RequestFactory:
    """Design Pattern Factory para devolver custom requests"""
    @staticmethod
    def makeRequest(message, server_info):
        if message.method == "GET":
            return ResponseGet(message, server_info)
        elif message.method == "POST":
            return ResponsePost(messag, server_info)
        elif message.method == "PUT":
            return ResponsePut(message, server_info)

class Response(ABC):
    def __init__(self, message, server_info):
        self.protocol  = message.protocol
        self.hostname  = server_info[1]
        self.system    = server_info[0]
        self.root_path = f".{self.hostname}/"
        # Date  = "Date" ":" HTTP-date
        self.date = date.today().strftime("%a, %d %b %Y %H:%M:%S %Z")
        self.checkRoot(self.root_path)
        self.response = "HTTP/1.1 {} {}\n\rServer: {}\n\rContent-Type: {}; charset=utf-8\n\rDate: {}\n\r"
        
    # if there isn`t a root directory, create one
    # raise an exception if that's impossible to do
    # IMPLEMENT EXCEPTION
    def checkRoot(self, root):
        if not os.path.isdir(root):
            os.mkdir(root)

    def checkProtocol(self):
        pass
    
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
