class Message:
    def __init__(self, msg):
        self.__parse__(msg)

    def __parse__(self, msg):
        parsedMsg      = msg.replace("\n", " ").split(" ")
        size = len(parsedMsg)
        self.method    = parsedMsg[0] if size >= 1 else ""
        self.request   = parsedMsg[1] if size >= 2 else ""
        self.protocol  = parsedMsg[2] if size >= 3 else ""
        self.host      = parsedMsg[4] if size >= 5 else ""
        self.userAgent = parsedMsg[6] if size >= 7 else ""
        self.accept    = parsedMsg[9] if size >= 10 else ""

    def __str__(self):
        return f"""Method: {self.method}
Request: {self.request}
Protocol: {self.protocol}
Host: {self.host}
User-Agent: {self.userAgent}
Accept: {self.accept}"""
