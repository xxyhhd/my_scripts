from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
from mysql_scripts.check_mysql_process import check_mysqld_porcess


def remove_mysql(host, port):
    console.print('开始删除主机实例：{0}:{1}'.format(host, port), style="bold yellow")
    console.print('开始清理实例进程', style="bold yellow")
    while True:
        mysql_proc_info =  check_mysqld_porcess(host, port)
        if mysql_proc_info:
            console.print('kill命令为：{0}'.format(mysql_proc_info), style="bold red")
            kill_ok = input("\033[5;34m{0}\033[0m".format('请确认kill命令是否正确(yes or no)：'))
            if kill_ok == 'yes':
                ssh_cli(host, mysql_proc_info)
            else:
                break
        else:
            console.print('进程不存在或已经清理！！！！', style="bold yellow")
            break
    console.print('开始清理实例文件', style="bold yellow")
    ssh_cli(host, 'rm -fr /dbs/mysqls/mysql{0}'.format(port))

