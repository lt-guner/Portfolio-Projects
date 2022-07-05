import socket
import pickle
from time import sleep
from .constants import *


class Payload:
    def __init__(self, data):
        self.data = data


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
            return pickle.loads(self.client.recv(2048))
        except:
            print("ERROR")
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            self.client.close()

    def receive(self):
        try:
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            self.client.close()

    def close(self):
        self.client.close()
