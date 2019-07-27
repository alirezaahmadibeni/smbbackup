import os
from configparser import SafeConfigParser


def getConnectionInfo():
    config_filename = os.path.join(os.path.dirname(__file__), 'connection.ini')
    cp = SafeConfigParser()
    cp.read(config_filename)

    info = {
        'server_name': cp.get('server', 'name'),
        'server_ip': cp.get('server', 'ip'),
        'server_port': cp.getint('server', 'port'),
        'client_name': cp.get('client', 'name'),
        'user': cp.get('user', 'name'),
        'password': cp.get('user', 'password'),
        'domain': cp.get('user', 'domain'),
        'BASE_DIR': cp.get('directory', 'base_dir'),
        'share_name': cp.get('directory', 'share_name'),
        'log_file': cp.get('directory', 'log_file')
    }
    return info

# print(getConnectionInfo())
