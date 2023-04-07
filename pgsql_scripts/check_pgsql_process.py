from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console


def check_pgsql_porcess(host, port):
    pgsql_proc_info = ssh_cli(host, 'ps -ef |grep "dbs/pgsql/pgsql{}/data" |grep -v grep'.format(port))[0]
    if pgsql_proc_info == '':
        return False  
    else:
        print(pgsql_proc_info)
        pgsql_process_num = ssh_cli(host, "ps -ef |grep 'dbs/pgsql/pgsql%s/data' |grep -v grep | awk '{print $2}'"%(port))[0].strip()
        pgsql_kill_cmd = 'kill -9 {};'.format(pgsql_process_num)
        return(pgsql_kill_cmd)

