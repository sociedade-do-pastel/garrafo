import socket as sokt

connection = ("127.0.0.1", 8080)

def main():
    with sokt.socket(sokt.AF_INET, sokt.SOCK_STREAM) as sock:
        sock.connect(connection)
        sock.sendall(bytes("jaaj jooj".encode("UTF-8")))

main()
