
from socket import socket, SOCK_STREAM, AF_INET


class TCPClient:
    def __init__(self, address: str, port: int):
        self.host = (address, port)

    def test(self, message: str, stop_message: str = "STOP"):

        # Create client
        client = socket(AF_INET, SOCK_STREAM)

        client.connect(self.host)

        # Disable blocking
        client.setblocking(False)

        response_size = client.send(message.encode('utf-8'))
        print(f'Amount of data received in non-blocking mode: {response_size}')

        client.send(stop_message.encode('utf-8'))
        client.close()


if __name__ == "__main__":

    from json import load

    with open("host_info.json", "rt") as f:
        info = load(f)

    client = TCPClient(info["address"], info["port"])
    client.test("Hello from client!!!")
