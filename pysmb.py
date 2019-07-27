from smb.SMBConnection import SMBConnection
from util import getConnectionInfo
import datetime
import os
from smb import smb_structs
from nmb.NetBIOS import NetBIOS
import sys
from daemon import Daemon
import time


def getBIOSName(remote_smb_ip, timeout=30):
    try:
        bios = NetBIOS()
        srv_name = bios.queryIPForName(remote_smb_ip, timeout=timeout)
    except:
        print(sys.stderr, "Looking up timeout, check remote_smb_ip again!!")
    finally:
        bios.close()
        return srv_name


def smbwalk(conn, shareddevice, top=u'/'):
    dirs, nondirs = [], []

    if not isinstance(conn, SMBConnection):
        raise TypeError("SMBConnection required")

    names = conn.listPath(shareddevice, top)

    for name in names:
        if name.isDirectory:
            if name.filename not in [u'.', u'..']:
                dirs.append(name.filename)
        else:
            nondirs.append(name.filename)

    yield top, dirs, nondirs

    for name in dirs:
        new_path = os.path.join(top, name)
        for x in smbwalk(conn, shareddevice, new_path):
            yield x


info = getConnectionInfo()
smb_structs.SUPPORT_SMB2 = smb_structs.SUPPORT_SMB2x = True
"""
 problems
 
 if connection reset by peer in windows file sharing the server_name is important for SMBConnection
 we get server name by getBIOSName function and set to smb object


"""
BASE_DIR = info['BASE_DIR']

log_file = open(os.path.join(BASE_DIR, info['log_file']), "a")

conn = SMBConnection(info['user'], info['password'], info['client_name'], getBIOSName(info['server_ip'])[0],
                     use_ntlm_v2=True, domain=info['domain'])
assert conn.connect(info['server_ip'], info['server_port'])

ans = smbwalk(conn, info['share_name'], top='/')

for tup in ans:
    for root, dirs, files in ans:
        if not os.path.isdir(BASE_DIR + root):
            os.mkdir(BASE_DIR + root)
        """
            Now Check all files is exists if not exits we need get files over the smb protocol
            and save they in backup folder
        """
        for file in files:
            if not os.path.isfile(os.path.join(BASE_DIR + root, file)):
                log_file.write(
                    "BACKUP DATE : " + str(datetime.datetime.now()) + " : =====> " + os.path.join(BASE_DIR + root,
                                                                                                  file) + "\n")
                with open(os.path.join(BASE_DIR + root, file), 'wb') as fi:
                    conn.retrieveFile(info['share_name'], os.path.join(root, file), fi)

log_file.close()


class BackupDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(10)
            log_file = open(os.path.join(BASE_DIR, info['log_file']), "a")
            log_file.write("this is test")
            log_file.close()
