import socket as sokt

connection = ("", 8080)

def parsing(msg):
    pass

def conEstablished(soos):
    "Process the protocol after connection established."
    while True:
        conSocket, addr = soos.accept()
        #implementar log aqui

        mensagem = conSocket.recv(2048).decode("UTF-8")
        print(mensagem)
        

def main():
    with sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM) as sock:
        sock.bind(connection)
        sock.listen(1)

        print("Conexão HTTP/1.1 estabelecida!")
        conEstablished(sock)

main()
