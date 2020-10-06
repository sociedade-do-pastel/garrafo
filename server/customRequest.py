from abc import ABC, abstractmethod

class RequestFactory:
    """Design Pattern Factory para devolver custom requests"""
    @staticmethod
    def makeRequest(message):
        if message.method == "GET":
            return ResponseGet(message)
        elif message.method == "POST":
            return ResponsePost(message)
        elif message.method == "PUT":
            return ResponsePut(message)

class Response(ABC):
    def __init__(self, message):
        self.protocol = message.protocol

    @abstractmethod
    def makeResponse(self):
        pass

class ResponseGet(Response):
    def __init__(self, message):
        super().__init__(message)

    
    def makeResponse(self):
        pass

class ResponsePost(Response):
    def __init__(self, message):
        super().__init__(message)
    
    def makeResponse(self):
        pass

class ResponsePut(Response):
    def __init__(self, message):
        super().__init__(message)

    def makeResponse(self):
        pass
