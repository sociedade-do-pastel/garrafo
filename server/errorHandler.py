# definition for the html code which
# is gonna be used as a template for all
# our errors
error_markdown = '''<!DOCTYPE html>
<html>
<head><title>{:}</title></head>
<body>
<br>
<h1>{:}</h1>
<p>{:}</p>
<img src=\"{:}\">
</body>
</html>'''

class GeneralError(Exception):
    def __init__(self, error_code, error, rundown, image):
        self.error_code = error_code
        self.error_mime = "text/html ; charset=utf-8"
        self.error_message = error
        self.rundown = rundown
        self.image = image
        self.error_body = bytes(error_markdown.format(self.error_message, self.error_message, self.rundown, self.image).encode("UTF-8"))
        self.error_length = len(self.error_body)

class ServerError(GeneralError):
    def __init__(self):
        super().__init__(500,
                         "500 Internal Server Error",
                         "Server encountered an error and seems to be inoperable.",
                         "https://cdn0.vox-cdn.com/thumbor/qtENVA_fBEiDYPj8wdSZRLcP7bQ=/110x0:565x303/1200x800/filters:focal(110x0:565x303)/cdn0.vox-cdn.com/uploads/chorus_image/image/50310263/658.0.0.png")

class HTTPnotSupported(GeneralError):
    def __init__(self):
        super().__init__(505,
                         "505 HTTP Version Not Supported",
        '''
        The server does not support, or refuses to support, 
        the HTTP protocol version that was used in the request message. 
        The server is indicating that it is unable or unwilling to complete the request
        using the same major version as the client. 
        Our job was to implement HTTP/1.1 :^)''',
        "https://i.kym-cdn.com/photos/images/facebook/001/483/348/bdd.jpg")


class NotFound(GeneralError):
    def __init__(self):
        super().__init__(404,
                         "404 Not Found",
                         "The server has not found anything matching the Request-URI. No indication is given of whether the condition is temporary or permanent.",
                         "https://moriyashrine.org/uploads/monthly_2019_08/large.Cir_Read.png.6801b7801f20f720749bc8c4eafd301a.png")


class BadRequest(GeneralError):
    def __init__(self):
        super().__init__(400,
                         "400 Bad Request",
                          "The request could not be understood by the server due to malformed syntax.",
                         "https://moriyashrine.org/uploads/monthly_2019_08/large.Cir_No.jpg.61eed7630ca587cfa326e87885068d51.jpg")


class MovedPerm(GeneralError):
    def __init__(self, new_path):
        super().__init__(301,
                         "301 Moved Permanentely",
                         f"The requested resource has been assigned a new permanent URI and any future references to this resource SHOULD use one of the returned URIs. The new path should be {new_path}",
                         "https://i.redd.it/5o5o2rdgt2oz.jpg")
                         
    
        
