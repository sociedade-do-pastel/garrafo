class Message:
    def __init__(self, msg):
        self.method = ""
        self.request = ""
        self.protocol = ""
        self.host = ""
        self.user_agent = ""
        self.accept = ""
        self.__parse__(msg)

    def __parse__(self, msg):
        # Request-Line   = Method SP Request-URI SP HTTP-Version CRLF
        parsedMsg      = msg.split("\n")
        for x in parsedMsg:
            y = x.split(" ")
            if y[0] in ["GET", "POST", "PUT"]:
                self.method, self.request, self.protocol = y
                self.protocol = self.protocol[:-1]
            elif y[0] == "Host:":
                self.host = y[1][:-1]
            elif y[0] == "User-Agent:":
                self.user_agent = y[1:len(y)]
            elif y[0] == "Accept:":
                self.accept = y[1][:-1]

    def __str__(self):
        return f"""Method: {self.method}
Request: {self.request}
Protocol: {self.protocol}
Host: {self.host}
User-Agent: {self.user_agent}
Accept: {self.accept}"""
