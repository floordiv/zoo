from shlex import split
from subprocess import Popen, PIPE

from syst.tools.output import println


def run(cmd, reader, path='.'):
    println('PROCESS', 'Started process: ' + cmd)

    with Popen(split(cmd), stdout=PIPE, stderr=PIPE, cwd=path) as proc:
        while True:
            char = proc.stdout.read(1)

            if char == b'' and proc.poll() is not None:
                break

            reader.write(char.decode())

    println('PROCESS', f'Process finished with exit-code {proc.returncode}: {cmd}')

    reader.finished = True
    reader.returncode = proc.returncode
