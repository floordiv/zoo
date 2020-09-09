from json import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM

from mproto import sendmsg, recvmsg


class NotConnected(Exception):
    ...


class Plugin:
    def __init__(self, addr):
        self.addr = addr

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.connected = False

    def connect(self):
        self.sock.connect(self.addr)
        self.connected = True

    def request(self, request_type, request_data=None, wait_response=True):
        if not self.connected:
            raise NotConnected()

        packet = dumps({'type': request_type, 'data': request_data})

        sendmsg(self.sock, packet.encode())

        if wait_response:
            return loads(recvmsg(self.sock).decode())
