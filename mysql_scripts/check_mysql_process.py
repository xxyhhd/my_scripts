from tools.tool_cmd import ssh_cli
# from rich.console import Console
from generic_scripts.gen_class import console


# console = Console()


def check_mysqld_porcess(host, port):
    mysql_proc_info = ssh_cli(host, 'ps -ef |grep mysqld |grep {} |grep -v grep'.format(port))[0]
    if mysql_proc_info == '':
        return False  
    else:
        print(mysql_proc_info)
        process_num = ssh_cli(host, "ps -ef |grep mysqld |grep %s |grep -v grep |awk '{print $2}'"%(port))[0].split()
        kill_cmd = ''
        for x in process_num:
                kill_cmd = kill_cmd + 'kill -9 ' + x + ';'
        return(kill_cmd)

