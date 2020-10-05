import socket
from sys import argv
from json import loads
from time import sleep

import mproto


if len(argv) < 3:
    print('Error: bad syntax. Try python3 service_output.py <ip> <service-name>')
    exit()


sock = socket.socket()
sock.connect((argv[1], 7777))

while True:
    mproto.sendmsg(sock, b'{"type": "get-output-updates", "data": "%s"}' % argv[2].encode())
    response = mproto.recvmsg(sock)
    jsonified_response = loads(response.decode())

    if not jsonified_response['succ']:
        print(jsonified_response['data'])
        break

    if jsonified_response['data']:
        print(*jsonified_response['data'], sep='\n')

    sleep(0.5)
