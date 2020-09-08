import syst.mworker as mworker


@mworker.handler(lambda packet: packet.header == 'say')
def handler(server, packet):
    server.send(packet, {'succ': True, 'data': packet.data})
