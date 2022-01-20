from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from Person import person

#Gobal constants
HOST = ''
PORT = 5001
BUFSIZ = 500
MAX_CONNETIONS = 20
ADDR = (HOST, PORT)
Persons = []

#Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server


def broadcast(name, msg):
    """Broadcast the message to all clients"""
    for person in Persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as x:
            print("[EXCEPTION]", x)


def communicating_with_client(Persons):
    """handle the messages from the client"""
    client = Persons.client

    name = client.recv(BUFSIZ).decode("utf8")
    Persons.set_name(name)

    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, " ")

    while True:
        msg = client.recv(BUFSIZ)

        if msg == bytes("{quit}", "utf8"):
            client.close()
            Persons.remove(Persons)
            broadcast(bytes(f"has left the chat", "utf8"), " ")
            print(f"[DISCONNECTED] {name} is disconnected")
            break
        else:
            broadcast(msg, name+ ": ")
            print(f"{name}:", msg.decode("utf8"))


def waiting_for_connections():
    """wait for connections from client"""
    while True:
        try:
            client, addr = SERVER.accept()
            person = Persons(addr, client)
            person.append(person)

            print(f"[CONNECTIONS] {addr} has connected to the server at {time.time()}")
            Thread(target=communicating_with_client, agrs=(person,)).start()
        except Exception as x:
            print("[EXCEPTION]", x )
            break
        print ("THE SERVER HAS CRASHED")



if __name__ == "__main__":
    SERVER.listen(MAX_CONNETIONS)
    print("WAITING FOR CONNECTIONS...")
    ACCEPT_THREAD = Thread(target=waiting_for_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()