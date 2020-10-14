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
    connection = ("", int(sys.argv[1]))
except IndexError:
    connection = ("", DEFAULT_PORT)

def conEstablished(soos):
    "Process the protocol after connection established."
    conSocket, addr = soos.accept()
    print(f"Conectado com endereço {addr}")
    mensagem = conSocket.recv(2048).decode("UTF-8", "ignore")
    message_object = msg.Message(mensagem)
    # let's go with a bit of a verbose approach
    # here we accept the file that our client is sending
    if message_object.content_length is not None:
        conSocket.sendall(b"HTTP/1.1 200 Continue\r\nServer: Belfegor\r\nConnection: Keep-Alive\r\n\r\n")
        print(message_object.content_length)
        object_received = bytearray()
        
        control = int(message_object.content_length)
        while control > 0:
            object_received += conSocket.recv(2048)
            control -= 2048
            
    response_obj = RequestFactory.makeRequest(message_object, server_def, object_received)
    conSocket.sendall(bytes(response_obj.response.encode("UTF-8")))
    if response_obj.body is not None:
        conSocket.sendall(response_obj.body)

def main():
    "Initialize the database in case it doesn't exist"
    manageDatabase(server_def[1])
    with sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM) as sock:
        sock.bind(connection)
        print(f"Servidor rodando na porta {connection[1]}")
        sock.listen(True)
        conEstablished(sock)

main()
