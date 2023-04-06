from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
import time
import os


def start_redis(host, port):
    for timer in range(1, 4):
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep redis-server |grep :{} |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('第{0}次尝试启动，{1}:{2}'.format(timer, host, port), style="bold yellow")
            os.system('ssh {0} -t /dbs/redis/redis{1}/service/bin/redis-server /etc/redis{1}.conf &'.format(host, port))
            time.sleep(30)
        else:
            console.print('服务启动成功'.format(timer), style="bold green")
            return True    
    console.print('服务启动失败，请人工检查'.format(timer), style="bold green")
    return False



            
