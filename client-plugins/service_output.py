import socket
from json import loads
from time import sleep

import mproto


sock = socket.socket()
sock.connect(('127.0.0.1', 7777))

while True:
    mproto.sendmsg(sock, b'{"type": "get-output-updates", "data": "Test 1"}')
    response = mproto.recvmsg(sock)
    jsonified_response = loads(response.decode())

    if not jsonified_response['succ']:
        print(jsonified_response['data'])
        break

    if jsonified_response['data'] != ['']:
        print(jsonified_response['data'][0])

    sleep(0.5)
