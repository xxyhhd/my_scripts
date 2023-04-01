import os
from tools import ToolsCmd, get_db_package
import sys
from datetime import datetime
import time

db_v = sys.argv[1]
port = sys.argv[2]


def backup_all_mysql(db_v, port):
    bak_path = '/dbs/mysqls/backup/mysql{0}/{1}/'.format(port, datetime.now().strftime("%Y-%m-%d~%H:%M:%S"))
    ToolsCmd('mkdir -p {0}'.format(bak_path))
    print('开始备份成功，备份时间受实例大小影响，备份存放目录：{}'.format(bak_path))
    print(db_v)
    if 'mysql-5' in db_v:
        print(db_v)
        innobackupex = get_db_package('xtrabackup-2') + '/bin/innobackupex'
        os.system("{0} --defaults-file=/etc/my{1}.cnf --user=root --port={1} --password=123456 --host=172.17.0.1 --no-timestamp {2} 2>{2}bak.log ".format(innobackupex ,port, bak_path))
        time.sleep(1)
    elif 'mysql-8' in db_v:
        print(db_v)
        innobackupex = get_db_package('xtrabackup-8') + '/bin/xtrabackup'
        os.system("{0} --defaults-file=/etc/my{1}.cnf --user=root --port={1} --password=123456 --host=172.17.0.1 --backup --target-dir={2} 2>{2}bak.log".format(innobackupex ,port, bak_path))
        time.sleep(1)

backup_all_mysql(db_v, port)