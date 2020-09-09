import syst.mworker as mworker
from syst.types import Services, PersonalReader


lines_read = {}   # conn: lines_read


@mworker.handler(lambda packet: packet.header == 'get-services-names')
def get_services_list(server, packet):
    services = [service for service, reader in Services().get_all().items()]
    server.send(packet, {'succ': True, 'data': services})


@mworker.handler(lambda packet: packet.header == 'get-active-services')
def get_active_services(server, packet):
    server.send(packet, {'succ': True, 'data': Services().get_active()})


@mworker.handler(lambda packet: packet.header == 'get-output')
def get_output(server, packet):
    reader = Services().get(packet.data)

    if not reader:
        return server.send(packet, {'succ': False, 'data': 'service not found'})

    server.send(packet, {'succ': True, 'data': reader.output})


@mworker.handler(lambda packet: packet.header == 'get-output-updates')
def get_output_updates(server, packet):
    if packet.conn not in lines_read:
        lines_read[packet.conn] = 0

    reader = Services().get(packet.data)

    if not reader:
        return server.send(packet, {'succ': False, 'data': 'service not found'})
    if lines_read[packet.conn] + 1 == len(reader.output) and reader.finished:
        return server.send(packet, {'succ': False, 'data': 'service stopped'})

    update_lines = reader.output[lines_read[packet.conn]:]
    lines_read[packet.conn] += len(update_lines) - 1

    server.send(packet, {'succ': True, 'data': update_lines})


@mworker.handler(lambda packet: packet.header == 'get-services')
def get_services(server, packet):
    services = Services().get_all()
    all_services = []

    for name, reader in services.items():
        all_services.append({'name': name, **reader.serialize()})

    server.send(packet, {'succ': True, 'data': all_services})
