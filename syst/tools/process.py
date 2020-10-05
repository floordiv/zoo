from time import sleep
from shlex import split
from sys import stdout
from subprocess import Popen, PIPE

from syst.tools.output import println


def run(cmd, reader, path='.', autorestart=False, autorestart_timeout=.5):
    while True:
        println('PROCESS', f'[{reader.restarts}] Started process: ' + cmd)

        reader.finished = False
        reader.returncode = None

        with Popen(split(cmd), stdout=PIPE, stderr=stdout, cwd=path, encoding='utf-8') as proc:
            while not proc.poll():
                char = proc.stdout.read(1)

                if char == '':
                    break

                reader.write(char)

        println('PROCESS', f'[{reader.restarts}] {cmd}: finished with code {proc.returncode}')

        reader.writeline(f'---- finished (code: {proc.returncode}) ----\n\n')
        reader.finished = True
        reader.returncode = proc.returncode

        if not autorestart:
            return

        sleep(autorestart_timeout)
        reader.restarts += 1
