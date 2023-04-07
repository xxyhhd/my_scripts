from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
import time
import os


def start_pgsql(host, port):
    for timer in range(1, 4):
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep "dbs/pgsql/pgsql{}/data" |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('第{0}次尝试启动，{1}:{2}'.format(timer, host, port), style="bold yellow")
            ssh_cli(host, '/dbs/pgsql/pgsql{0}/service/bin/pg_ctl -D /dbs/pgsql/pgsql{0}/data -l logfile start'.format(port), username='pgsql{}'.format(port), password='pass1314')
            time.sleep(30)
        else:
            console.print('服务启动成功'.format(timer), style="bold green")
            return True    
    console.print('服务启动失败，请人工检查'.format(timer), style="bold green")
    return False



            
