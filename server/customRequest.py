"""Module reponsible for the specific requests and it's errors."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from errorHandler import *
from fileHandler import *
import re

def checkProtocol(protocol_string):
    """Checks if protocol_string is HTTP/1.1, if not, raises HTTPnotsupported
error"""

    if protocol_string != "HTTP/1.1":
        raise HTTPnotSupported


class RequestFactory:
    """Design Pattern Factory to retrieve custom requests."""

    @staticmethod
    def makeRequest(message, server_info, object_received=None):
        """Checks the protocol and the method and retrieves the suited class
or error."""
        
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
    """Response class forces every sub-class to implement a makeResponse method"""

    def __init__(self, message, server_info):
        self.hostname = server_info[1]
        self.system = server_info[0] # currently unused
        # Date  = "Date" ":" HTTP-formatted-date
        self.date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %Z")
        self.response = "HTTP/1.1 {}\r\nServer: {}\r\nDate: {}\r\nConnection: Keep-Alive\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n"
        self.body = None

    @abstractmethod
    def makeResponse(self):
        """Abstract method to handle the specific class response part."""


class ResponseGet(Response):
    """Handles the GET Request."""

    def __init__(self, message, server_info):
        super().__init__(message, server_info)

        # searchFile returns an object containing message, mime-type, body and body length
        self.archive = searchFile(message.request, self.hostname)
        self.makeResponse()

    def makeResponse(self):
        self.response = self.response.format(self.archive.message,
                                             self.hostname,
                                             self.date,
                                             self.archive.mime,
                                             self.archive.length)
        self.body = self.archive.body

# should we delete this method?
class ResponsePost(Response):
    """Handles the POST Request."""

    def __init__(self, message, server_info):
        super().__init__(message, server_info)
        raise ServerError
    def makeResponse(self):
        pass


class ResponsePut(Response):
    def __init__(self, message, server_info, object_received):
        """Handles the PUT Request."""
        super().__init__(message, server_info)
        # PUT definition on the RFC2616 explicitely says that
        # our only responses are if a file was created or modified
        # therefore, createFile will only return if a file was moved (modified) or not
        self.makeResponse(message.request, createFile(message.request, object_received, self.hostname))

    def makeResponse(self, req, moved):
        if moved == 0:
            first_header  = f"201 Created\r\nContent-Location: {req}"
        else:
            first_header  = f"204 No Content\r\nContent-Location: {req}"
        self.response = self.response[0:(re.search(
            "[A-Za-z]ontent.*:", self.response)).span()[0]].format(
                first_header,
                self.hostname,
                self.date)

class ResponseError(Response):
    """Implementation of errors in Reponse format."""
    def __init__(self, message, error, server_info):
        super().__init__(message, server_info)
        self.makeResponse(error)

    def makeResponse(self, err):
        self.response = self.response.format(err.error_message,
                                             self.hostname,
                                             self.date,
                                             err.error_mime,
                                             err.error_length)
        self.body = err.error_body
