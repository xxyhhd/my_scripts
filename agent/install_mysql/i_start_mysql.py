from tools import ToolsCmd
import time
import os
from rich.console import Console


console = Console()



def check_mysql_process(port):
    return(ToolsCmd('ps -ef |grep mysqld |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip())


def start_mysql(port):
    console.print('\n8-开始起服务', style="bold yellow", highlight=True)
    os.system('/dbs/mysqls/mysql{0}/service/bin/mysqld_safe --defaults-file=/etc/my{0}.cnf & '.format(port))
    time.sleep(20)
    if check_mysql_process(port) == '2':
        console.print('服务启动成功', style="bold green", highlight=True)
        return True
    console.print('服务启动失败，请手动检查', style="bold red", highlight=True)
    return False