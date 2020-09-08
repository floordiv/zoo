from os import abort, environ

import syst.tools.servicestools as st


if __name__ == '__main__':
    environ['PYTHONUNBUFFERED'] = '1'

    all_service_files = st.get_service_files()
    services_configs = st.parse_service_files(all_service_files)
    st.run_services(services_configs)

    try:
        import syst.initsys
    except KeyboardInterrupt:
        print()
        abort()
