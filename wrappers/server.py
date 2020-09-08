import sys
import socket
from threading import Thread
from json import dumps, loads, JSONDecodeError

import syst.types as types
import syst.mworker as mworker
import syst.tools.mproto as mproto
from syst.tools.output import println


server = sys.modules[__name__]
addr = ('', 7777)


# I don't wanna catch KeyboardInterrupt in IfuckingDontKnowWhere, so, it's easier to make socket's object close-safe
class MySocket(socket.socket):
    def __del__(self):
        self.close()


sock = MySocket()


# TOOLS

def send(of_packet, data: dict):
    try:
        mproto.sendmsg(of_packet.conn, dumps(data).encode())
    except OSError:
        return


def recv(of_packet):
    return mproto.recvmsg(of_packet.conn)


# WORKERS

def accept_connections():
    while True:
        conn, addr = sock.accept()
        Thread(target=handle_connection, args=(conn,)).start()


def handle_connection(conn):
    ip, port = conn.getpeername()
    println('SERVER', f'{ip}:{port} - connected')

    try:
        while True:
            raw_packet = mproto.recvmsg(conn)

            if raw_packet == b'':
                raise BrokenPipeError

            try:
                packet = validate_packet(raw_packet)
            except (JSONDecodeError, UnicodeDecodeError):
                println('SERVER', f'{ip}:{port} - received invalid packet ({raw_packet})')
                continue

            packet_object = types.Packet(conn, packet['type'], packet['data'])
            mworker.process_update(server, packet_object, threaded=False, check_all=False)

    except (BrokenPipeError,):
        conn.close()
        println('SERVER', f'{ip}:{port} - disconnected')


def validate_packet(raw_packet):
    decoded = raw_packet.decode()
    jsonified = loads(decoded)

    if 'type' not in jsonified or 'data' not in jsonified:
        raise JSONDecodeError

    return jsonified


def init():
    try:
        sock.bind(addr)
    except OSError:
        ip, port = addr

        if ip == '':
            ip = 'global'

        return println('SERVER', f'{ip}:{port} - failed to init, already in use')

    sock.listen(0)
    Thread(target=accept_connections).start()
