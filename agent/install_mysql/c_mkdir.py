import os
from rich.console import Console


console = Console()


def mkdir(port):
    console.print('\n3-开始创建工作目录', style="bold yellow")
    os.system('mkdir -p /dbs/mysqls/mysql{0}/binlog'.format(port))
    os.system('mkdir -p /dbs/mysqls/mysql{0}/data'.format(port))
    os.system('mkdir -p /dbs/mysqls/mysql{0}/log'.format(port))
    os.system('mkdir -p /dbs/mysqls/mysql{0}/undo'.format(port))
    os.system('touch /dbs/mysqls/mysql{0}/log/mysql-error.log'.format(port))
    console.print('工作创建成功\n', style="bold green")