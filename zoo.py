from os import abort, environ

import syst.tools.servicestools as st


VERSION = '0.1.1'


if __name__ == '__main__':
    st.load_environ_settings(x)

    all_service_files = st.get_service_files()
    services_configs = st.parse_service_files(all_service_files)
    st.run_services(services_configs)

    try:
        import syst.initsys
    except KeyboardInterrupt:
        print()
        abort()