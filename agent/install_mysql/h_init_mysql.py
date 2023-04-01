from tools import ToolsCmd
import time
from rich.console import Console
import re

console = Console()


def init_mysql(port, db_v):
    console.print('\n7-开始初始化MySQL', style="bold yellow", highlight=True)

    if '5.6' in db_v:
        init_result = ToolsCmd('/dbs/mysqls/mysql{0}/service/scripts/mysql_install_db --defaults-file=/etc/my{0}.cnf --basedir=/dbs/mysqls/mysql{0}/service --datadir=/dbs/mysqls/mysql{0}/data --user=mysql'.format(port))
        time.sleep(15)
        for t in range(10):
            a =  ToolsCmd('ps -ef |grep mysql_install_db |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip() 
            if a == '0':
                break
            time.sleep(30)
        if  len(re.findall('OK', init_result[0])) == 2:
            console.print('MySQL初始化成功', style="bold green", highlight=True)
            return True

    else:
        ToolsCmd('/dbs/mysqls/mysql{0}/service/bin/mysqld --defaults-file=/etc/my{0}.cnf --initialize-insecure'.format(port))
        time.sleep(15)
        for t in range(10):
            a =  ToolsCmd('ps -ef |grep initialize |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip() 
            if a == '0':
                break
            time.sleep(30)
        if ToolsCmd('tail -1 /dbs/mysqls/mysql{0}/log/mysql-error.log |grep "empty password" |wc -l'.format(port))[0].rstrip() == '1':
            console.print('MySQL初始化成功', style="bold green", highlight=True)
            return True
    console.print('MySQL初始化失败', style="bold red", highlight=True)
    return False

