from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console


def check_redis_porcess(host, port):
    redis_proc_info = ssh_cli(host, 'ps -ef |grep redis-server |grep :{} |grep -v grep'.format(port))[0]
    if redis_proc_info == '':
        return False  
    else:
        print(redis_proc_info)
        redis_process_num = ssh_cli(host, "ps -ef |grep redis-server |grep :%s |grep -v grep | awk '{print $2}'"%(port))[0].strip()
        redis_kill_cmd = 'kill -9 {};'.format(redis_process_num)
        return(redis_kill_cmd)

