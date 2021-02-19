from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from json import load


with open("../host_info.json", "rt") as f:
    info = load(f)

BUFFER_SIZE = info["buffer_size"]

nickname = input("Enter your nickname: ")

client = socket(AF_INET, SOCK_STREAM)
client.connect((info["address"], info["port"]))


def receive():
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)

        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input(">>> ")}'
        client.send((message.encode('utf-8')))


receive_thread = Thread(target=receive)
receive_thread.start()

write_thread = Thread(target=write)
write_thread.start()
