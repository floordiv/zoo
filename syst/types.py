from json import dumps

from syst.tools.configreader import load


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)

        return instances[class_]

    return getinstance


class Packet:
    def __init__(self, conn, header, data):
        self.conn = conn
        self.header = header
        self.data = data


class Config:
    def __init__(self, path):
        data = load(path, ignore_case=True)

        for key, value in data.items():
            setattr(self, key, value)


class Reader:
    def __init__(self):
        self.output = ['']
        self.finished = False
        self.returncode = None

    def write(self, char, **kwargs):
        if char == '\n':
            return self.output.append('')

        self.output[-1] += char

    def serialize(self):
        return {'out': '\n'.join(self.output),
                'finished': self.finished,
                'returncode': self.returncode}

    def de_serialize(self, data):
        self.output = data['out'].splitlines()
        self.finished = data['finished']
        self.returncode = data['returncode']

    def __str__(self):
        return dumps(self.serialize(), indent=2)

    def readlines(self, n=1):
        return self.output[-n:]


class PersonalReader:
    def __init__(self):
        self.buffer = []

    def writelines(self, lines):
        self.buffer.extend(lines)

        return self

    def readlines(self, n=1):
        if not self.buffer:
            return []

        lines = self.buffer[:n]
        del self.buffer[:n]

        return lines


@singleton
class Services:
    def __init__(self, services=None):
        if services is None:
            services = {}   # service_name: reader

        self._services = services

    def get_all(self):
        return self._services

    def get(self, name):
        return self._services.get(name)

    def add(self, name, reader):
        assert name not in self._services    # re-writing existing service is bad idea

        self._services[name] = reader

    def remove(self, name):
        assert name in self._services

        del self._services[name]

    def get_active(self):
        return [service for service, reader in self._services.items() if not reader.finished]

    def get_finished(self):
        active = self.get_active()
        return [service for service in self._services if service not in active]

    def get_finished_with_errors(self):
        return [service for service, reader in self._services if reader.finished and reader.returncode != 0]

    def __str__(self):
        return f'Services(_services={self._services})'
