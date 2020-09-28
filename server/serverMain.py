import socket as sokt
import message as msg

connection = ("", 8080)

def conEstablished(soos):
    "Process the protocol after connection established."
    while True:
        conSocket, addr = soos.accept()
        print(f"Conectado com endereço {addr}")

        mensagem = conSocket.recv(2048).decode("UTF-8")
        mensagem = msg.Message(mensagem)
        print(mensagem)

def main():
    with sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM) as sock:
        sock.bind(connection)
        sock.listen(1)

        conEstablished(sock)

main()
