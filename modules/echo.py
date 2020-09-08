import syst.mworker as mworker


@mworker.handler(lambda packet: packet.header == 'echo')
def simple_echo(server, packet):
    server.send(packet, {'succ': True, 'response': 'hello from deti Donbassa'})
