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
    response_obj = RequestFactory.makeRequest(msg.Message(mensagem), server_def)
    conSocket.sendall(bytes(response_obj.response.encode("UTF-8")))
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
