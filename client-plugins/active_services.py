import socket
from json import loads

import mproto


sock = socket.socket()
sock.connect(('127.0.0.1', 7777))

mproto.sendmsg(sock, b'{"type": "get-active-services", "data": null}')
response = mproto.recvmsg(sock)
jsonified_response = loads(response.decode())
print(jsonified_response)
