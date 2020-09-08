import socket
import struct


def sendmsg(conn, data):
    """
    @type conn: socket.socket
    @type data: str
    """

    bytelike_source = bytes(data)
    msg_len = struct.pack('>I', len(bytelike_source))

    conn.send(msg_len)
    conn.recv(1)    # wait for client approving. 4 bytes is enough (we don't need too much)
    conn.send(bytelike_source)


def recvmsg(conn):
    """
    @type conn: socket.socket
    """

    raw_msglen = conn.recv(4)

    if not raw_msglen or len(raw_msglen) != 4:
        return b''

    msg_len = struct.unpack('>I', raw_msglen)[0]  # [0] cause struct.unpack returns tuple

    conn.send(b'\x01')    # we received and processed new message, so, let's approve it for server

    # it's time to receive our message!
    received_message = b''

    while len(received_message) < msg_len:
        received_message += conn.recv(msg_len - len(received_message))

    return received_message   # I don't care, decode it by yourself.
