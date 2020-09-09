from os import system
from time import sleep

from plugin import Plugin


plugin = Plugin(('127.0.0.1', 7777))
plugin.connect()


while True:
    response = plugin.request('get-services')

    if not response['succ']:
        print('Server returned error:', response['data'])
        break

    for service in response['data']:
        if service['finished']:
            print(f'[{service["name"]}]: inactive (finished with code {service["returncode"]})')
        else:
            print(f'[{service["name"]}]: active')

    sleep(0.2)
    system('clear')
