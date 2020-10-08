from customRequest import *
import socket as sokt
import message as msg
import os

# uname could give me both system where the server is running
# and hostname
#
# [0]: OS; [1]: hostname; [-1]: cpu architecture
server_def = os.uname()

connection = ("", 8081)

def conEstablished(soos):
    "Process the protocol after connection established."
    conSocket, addr = soos.accept()
    print(f"Conectado com endereço {addr}")
    mensagem = conSocket.recv(2048).decode("UTF-8", "ignore")
    response_obj = RequestFactory.makeRequest(msg.Message(mensagem), server_def)
    conSocket.sendall(bytes(response_obj.response.encode("UTF-8")))


def main():
    with sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM) as sock:
        sock.bind(connection)
        print("Servidor rodando")
        sock.listen(True)
        conEstablished(sock)

main()
