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
    return parse_service_files(argv[1:])


def parse_service_files(files):
    output_files = []

    for file in files:
        file = file.strip()

        if file.endswith('.pack'):
            with open(file) as packfile:
                output_files.extend(parse_service_files(packfile))
        elif file.endswith('.service'):
            output_files.append(file)
            println('ZOO:services', f'Added service file: {file}')
        else:
            println('ZOO:warning', f'Warning: "{file}": unknown extension. Skipped')

    return output_files


def fill_service_file(config, fill_by: dict):
    for var, defailt_val in fill_by.items():
        if not hasattr(config, var):
            setattr(config, var, defailt_val)

    return config


def cook_service_files(service_files):
    cooked_services = []

    for file in service_files:
        file = expanduser(file)
        file_dirname = dirname(file)

        try:
            service = Config(file)
        except FileNotFoundError:
            println('ZOO', f'Error: service-file "{file}" not found')
            continue

        if not hasattr(service, 'cmd'):
            println('ZOO', f'Error: service-file "{file}" does not contains "cmd" value')
            continue

        fill_by = {
            'path': file_dirname if file_dirname else './',
            'name': basename(file)[:-len('.service')],
            'autorestart': False,
            'restart_timeout': .5,
            'output_maxlines': 1000,
        }
        service = fill_service_file(service, fill_by)

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
        reader = Reader(service.output_maxlines)
        services.add(service.name, reader)
        Thread(target=run_process, args=(service.cmd, reader), kwargs={'path': service.path,
                                                                       'autorestart': service.autorestart,
                                                                       'autorestart_timeout': service.restart_timeout}).start()
