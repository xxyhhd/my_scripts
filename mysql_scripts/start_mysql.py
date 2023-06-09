from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
import time
import os


def start_mysql(host, port):
    for timer in range(1, 4):
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep mysqld |grep {} |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('第{0}次尝试启动，{1}:{2}'.format(timer, host, port), style="bold yellow")
            os.system('ssh {0} -t /dbs/mysqls/mysql{1}/service/bin/mysqld_safe --defaults-file=/etc/my{1}.cnf & '.format(host, port))
            time.sleep(30)
        else:
            console.print('服务启动成功'.format(timer), style="bold green")
            return True    
    console.print('服务启动失败，请人工检查'.format(timer), style="bold green")
    return False



            
