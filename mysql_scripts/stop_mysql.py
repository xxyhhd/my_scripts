from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
import time


def stop_mysql(host, port):
    for timer in range(1, 4):
        console.print('第{0}次尝试停止，{1}:{2}'.format(timer, host, port), style="bold yellow")
        cmd_stop = '/dbs/mysqls/mysql{0}/service/bin/mysqladmin -uroot -P{0} -p123456 -h127.0.0.1 shutdown'.format(port)
        ssh_cli(host, cmd_stop)
        time.sleep(30)
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep mysqld |grep {} |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('停止成功'.format(timer), style="bold green")
            return False  
    console.print('服务停止失败，请人工检查'.format(timer), style="bold green")
   
        