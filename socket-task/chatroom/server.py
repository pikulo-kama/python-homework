from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from json import load

with open("../host_info.json", "rt") as f:
    info = load(f)

server = socket(AF_INET, SOCK_STREAM)
server.bind((info["address"], info["port"]))
server.listen()

clients = []
nicknames = []

BUFFER_SIZE = info["buffer_size"]


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(BUFFER_SIZE)
            broadcast(message)

        except Exception:
            remove_chat_user(client)
            break


def remove_chat_user(client):
    index = client.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast(f' {nickname} left the chat!'.encode('utf-8'))
    nicknames.remove(nickname)


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(BUFFER_SIZE).decode('utf-8')
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server'.encode('utf-8'))

        thread = Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening.....")
receive()
