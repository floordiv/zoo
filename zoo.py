from sys import argv
from os import abort
from subprocess import Popen, PIPE

from syst.tools.output import println
import syst.tools.servicestools as st


VERSION = '0.9.7'


def main():
    st.load_environ_settings()
    st.push_pid()

    all_service_files = st.get_service_files()

    if not all_service_files:
        if '-pack' not in argv:
            println('ZOO:error', 'No service files given')
        else:
            println('ZOO:error', 'services pack does not contains any service files')

        exit()

    services_configs = st.cook_service_files(all_service_files)
    st.run_services(services_configs)

    try:
        import syst.initsys
    except KeyboardInterrupt:
        print()
        abort()


if __name__ == '__main__':
    if '--nondaemon' in argv:
        argv.remove('--nondaemon')
        main()
    else:
        Popen(['python3'] + argv + ['--nondaemon'], stdout=PIPE, stderr=PIPE)
