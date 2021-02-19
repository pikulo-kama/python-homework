
from socket import socket, SOCK_STREAM, AF_INET
from json import load


with open("host_info.json", "rt") as f:
    info = load(f)

BUFFER_SIZE = info["buffer_size"]


class TCPServer:

    def __init__(self, address: str, port: int):
        self.host = (address, port)

    def start(self):

        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(self.host)
        server_socket.listen(5)

        print('The server is waiting for connection...')

        while True:
            client, client_address = server_socket.accept()
            client_message = client.recv(BUFFER_SIZE)

            while client_message:
                print(f'{client_address}: {client_message.decode("utf-8")}')
                client_message = client.recv(BUFFER_SIZE)

            print("All data received")
            client.close()
            break


if __name__ == "__main__":
    server = TCPServer(info["address"], info["port"])
    server.start()
