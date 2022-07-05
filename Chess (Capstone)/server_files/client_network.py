import socket
from time import sleep
from constants import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVER, PORT)
        self.connected = False

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(CONN_SUCCESS)
            self.connected = True
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            self.reconnect()

    def receive(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            self.reconnect()

    def reconnect(self):
        print(LOST_CONN_RECONN)
        try:
            client.connect(self.addr)
            print(RECONN_SUCCESS)
        except socket.error:
            sleep(2)
