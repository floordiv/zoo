from sys import argv
from os import environ
from threading import Thread
from os.path import dirname, basename, expanduser

from syst.tools.output import println
from syst.tools.configreader import load
from syst.types import Config, Reader, Services
from syst.tools.process import run as run_process


services = Services()


def get_service_files():
    if '-pack' in argv:
        pack_file = argv[argv.index('-pack') + 1].strip('"').strip("'")  # remove quotes if they exists

        with open(pack_file) as pack:
            return [file.rstrip() for file in pack if file.rstrip().endswith('.service')]

    return [file for file in argv[1:] if file.endswith('.service')]


def parse_service_files(service_files):
    cooked_services = []

    # print(service_files)

    for file in service_files:
        file = expanduser(file)

        try:
            service = Config(file)
        except FileNotFoundError:
            print(f'[ZOO] Error: service-file "{file}" not found')
            continue

        if not hasattr(service, 'path') or service.path == '.':
            file_path = dirname(file)

            if not file_path:
                file_path = './'

            service.path = file_path

        if not hasattr(service, 'name'):
            service.name = basename(file)[:-len('.service')]

        if not hasattr(service, 'cmd'):
            print(f'[ZOO] Error: service-file "{file}" does not contains "cmd" value')
            continue

        service.path = expanduser(service.path)
        cooked_services.append(service)

    return cooked_services


def load_environ_settings(file='syst/environ.settings'):
    try:
        environ_config = load(file, ignore_case=False, parse_types=False)

        for key, value in environ_config.items():
            environ[key] = str(value)
    except FileNotFoundError:
        println('LOAD-ENV-SETTINGS', f'Failed: "{file}" not found')


def run_services(services_list):
    for service in services_list:
        reader = Reader()
        services.add(service.name, reader)
        Thread(target=run_process, args=(service.cmd, reader), kwargs={'path': service.path}).start()
