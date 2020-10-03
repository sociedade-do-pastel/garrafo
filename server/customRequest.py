from abc import ABC, abstractmethod

class RequestFactory:
    """Design Pattern Factory para devolver custom requests"""
    @staticmethod
    def makeRequest(message):
        if message.method == "GET":
            return ResponseGet(message)

class Response(ABC):
    def __init__(self, message):
        self.protocol = message.protocol

    @abstractmethod
    def makeResponse(self):
        pass

class ResponseGet(Response):
    def __init__(self, message):
        pass

class ReponsePost(Response):
    def __init__(self, message):
        pass

class ResponsePut(Response):
    def __init__(self, message):
        pass
