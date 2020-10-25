from customRequest import *
from fileHandler import *
import socket as sokt
import message as msg
import os
import sys

# [0]: OS; [1]: hostname
server_def = (os.name, sokt.gethostname())
# value for a default port if our user doesn't define one
DEFAULT_PORT = 8080
try:
    connection = ("", int(sys.argv[1])) # note that if a proper string isn't passed, the server will surely crash
except IndexError:
    connection = ("", DEFAULT_PORT)

def conEstablished(soos):
    "Generate a correct string of messages after the connection has been established."
    conSocket, addr = soos.accept()
    print(f"Connected with address: {addr}")

    mensagem = ""
    while True:
        mensagem += conSocket.recv(2048).decode("UTF-8", "ignore")
        if mensagem[-3:] == "\n\r\n":
            break

    message_object = msg.Message(mensagem)
    object_received = bytearray()
    # let's go with a bit of a verbose approach
    # here we accept the file that our client is sending IF content-length
    # was declared within their request
    if message_object.content_length is not None:
        conSocket.sendall(bytes("HTTP/1.1 200 Continue\r\nServer: {}\r\n\r\n".format(server_def[1]).encode("UTF-8")))
        control = int(message_object.content_length)
        while control > 0:
            object_received += conSocket.recv(2048)
            control -= 2048 # our received chunks must be 2048 bytes long
    
    response_obj = RequestFactory.makeRequest(message_object, server_def, object_received)
    conSocket.sendall(bytes(response_obj.response.encode("UTF-8")))
    # finally, send our body if it exists
    if response_obj.body is not None:
        conSocket.sendall(response_obj.body)

def main():
    "main function where our loop happens"
    #Initialize the database in case it doesn't exist
    manageDatabase(server_def[1])
    with sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM) as sock:
        sock.bind(connection)
        print(f"Server running on port {connection[1]}")
        print("Press Ctrl-c to stop the current process")
        while True:
            sock.listen(True)
            conEstablished(sock)

main()
