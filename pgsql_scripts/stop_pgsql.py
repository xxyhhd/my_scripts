from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
import time


def stop_pgsql(host, port):
    for timer in range(1, 4):
        console.print('第{0}次尝试停止，{1}:{2}'.format(timer, host, port), style="bold yellow")
        ssh_cli(host, '/dbs/pgsql/pgsql{0}/service/bin/pg_ctl -D /dbs/pgsql/pgsql{0}/data -l logfile stop'.format(port), username='pgsql{}'.format(port), password='pass1314')
        time.sleep(30)
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep "dbs/pgsql/pgsql{}/data" |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('停止成功'.format(timer), style="bold green")
            return False  
    console.print('服务停止失败，请人工检查'.format(timer), style="bold green")
   
        