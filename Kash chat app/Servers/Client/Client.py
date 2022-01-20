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

    

