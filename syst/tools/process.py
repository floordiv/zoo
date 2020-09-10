from time import sleep
from shlex import split
from subprocess import Popen, PIPE

from syst.tools.output import println


def run(cmd, reader, path='.', autorestart=False, autorestart_timeout=.5):
    restarts = 1

    while True:
        println('PROCESS', f'[{restarts}] Started process: ' + cmd)

        reader.finished = False
        reader.returncode = None

        with Popen(split(cmd), stdout=PIPE, stderr=PIPE, cwd=path) as proc:
            while True:
                char = proc.stdout.read(1)

                if char == b'' and proc.poll() is not None:
                    break

                reader.write(char.decode())

        println('PROCESS', f'[{restarts}] Process finished with exit-code {proc.returncode}: {cmd}')

        reader.finished = True
        reader.returncode = proc.returncode
        restarts += 1

        if not autorestart:
            return

        sleep(autorestart_timeout)
