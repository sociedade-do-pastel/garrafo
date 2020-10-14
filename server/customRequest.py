from abc import ABC, abstractmethod
from datetime import date, time
from errorHandler import *
from fileHandler import *

def checkProtocol(protocol_string):
    if protocol_string != "HTTP/1.1":
        raise HTTPnotSupported


class RequestFactory:
    """Design Pattern Factory para devolver custom requests"""
    @staticmethod
    def makeRequest(message, server_info, object_received=None):
        root_path = "./{}".format(server_info[1])
        try:
            checkProtocol(message.protocol)
            if message.method == "GET":
                return ResponseGet(message, server_info)
            if message.method == "POST":
                return ResponsePost(message, server_info)
            if message.method == "PUT":
                return ResponsePut(message, server_info, object_received)
            raise BadRequest
        except GeneralError as err:
            return ResponseError(message, err, server_info)

class Response(ABC):
    def __init__(self, message, server_info):
        self.hostname = server_info[1]
        self.system = server_info[0]
        # Date  = "Date" ":" HTTP-date
        self.date = date.today().strftime("%a, %d %b %Y %H:%M:%S %Z")
        self.response = "HTTP/1.1 {}\r\nServer: {}\r\nDate: {}\r\nConnection: Keep-Alive\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n"
        self.body = None
    @abstractmethod
    def makeResponse(self):
        pass

class ResponseGet(Response):
    def __init__(self, message, server_info):
        super().__init__(message, server_info)
        
        # searchFile returns an object containing message, mime-type and body
        self.archive = searchFile(message.request, self.hostname)
        self.makeResponse()

    def makeResponse(self):
        self.response = self.response.format(self.archive.message, self.hostname,
                                              self.date, self.archive.mime, self.archive.length)
        self.body = self.archive.body

class ResponsePost(Response):
    def __init__(self, message, server_info):
        super().__init__(message, server_info)

    def makeResponse(self):
        pass

class ResponsePut(Response):
    def __init__(self, message, server_info, object_received):
        super().__init__(message, server_info)
        self.makeResponse(message.request, createFile(message.request, object_received, self.hostname))


    def makeResponse(self, req, moved):
        if moved == 0:
            self.response  = f"201 Created\r\nContent-Location: {req}\r\n"
        else:
            self.response  = f"204 No Content\r\nContent-Location: {req}\r\n"

class ResponseError(Response):
    def __init__(self, message, error, server_info):
        super().__init__(message, server_info)
        self.makeResponse(error)

    def makeResponse(self, err):
        self.response = self.response.format(err.error_message, self.hostname,
                                              self.date, err.error_mime, err.error_length)
        self.body = err.error_body
                                             

