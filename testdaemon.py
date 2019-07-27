from pysmb import BackupDaemon, BASE_DIR
import os

backup = BackupDaemon(os.path.join(BASE_DIR, 'pid.pid'))
backup.start()
