from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
from redis_scripts.check_redis_process import check_redis_porcess


def remove_redis(host, port):
    console.print('开始删除主机实例：{0}:{1}'.format(host, port), style="bold yellow")
    console.print('开始清理实例进程', style="bold yellow")
    while True:
        redis_proc_info =  check_redis_porcess(host, port)
        if redis_proc_info:
            console.print('kill命令为：{0}'.format(redis_proc_info), style="bold red")
            kill_ok = input("\033[5;34m{0}\033[0m".format('请确认kill命令是否正确(yes or no)：'))
            if kill_ok == 'yes':
                ssh_cli(host, redis_proc_info)
            else:
                break
        else:
            console.print('进程不存在或已经清理！！！！', style="bold yellow")
            break
    console.print('开始清理实例文件', style="bold yellow")
    ssh_cli(host, 'rm -fr /dbs/redis/redis{0}'.format(port))

