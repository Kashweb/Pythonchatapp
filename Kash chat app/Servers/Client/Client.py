from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

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


class client:
    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receivemessages(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCPETION]", e)
                break

    def sendmessage(self, msg):
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    
    def getmessage(self):
        messages_copy = self.messages[:]

        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy


    def disconnected(self):
        self.send_message("{quit}")

