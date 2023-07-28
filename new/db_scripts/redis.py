from generic_scripts.tools import ToolsCmd, ssh_cli
from generic_scripts.global_var import logger, console, dbaas
from nginx import set_nginx
import time
import re
import random
import inspect
import os



def login_redis(inst_info):
    norms = {1: 'master', 2: 'slave', 3: 'logger'}
    console.print('************** 请输入实例角色，提示：该实例只有{}个节点 **************'.format(len(inst_info)), style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    inst_role = input("\033[5;34m{0}\033[0m".format('默认登录主库：')) or '1'
    inst_role = int(inst_role) - 1
    if inst_role > len(inst_info) - 1:
        console.print('抱歉，该实例不存在所选角色', style="bold red")
        return False
    os.system('/home/redis/versions/redis-7.0.8/bin/redis-cli -h {0} -p {1}'.format(inst_info[inst_role][0], inst_info[inst_role][1]))


def start_redis(host, port):
    for timer in range(1, 4):
        redis_proc_info = ssh_cli(host, 'ps -ef |grep redis-server |grep :{} |grep -v grep'.format(port))[0]
        if redis_proc_info == '':
            console.print('第{0}次尝试启动，{1}:{2}'.format(timer, host, port), style="bold green")
            os.system('ssh {0} -t /dbs/redis/redis{1}/service/bin/redis-server /etc/redis{1}.conf &'.format(host, port))
            time.sleep(30)
        else:
            console.print('服务启动成功'.format(timer), style="bold green")
            return True    
    console.print('服务启动失败，请人工检查'.format(timer), style="bold green")
    return False


def stop_redis(host, port):
    for timer in range(1, 4):
        console.print('第{0}次尝试停止，{1}:{2}'.format(timer, host, port), style="bold green")
        cmd_stop = '/dbs/redis/redis{0}/service/bin/redis-cli -p {0} shutdown'.format(port)
        ssh_cli(host, cmd_stop)
        time.sleep(30)
        redis_proc_info = ssh_cli(host, 'ps -ef |grep redis-server |grep :{} |grep -v grep'.format(port))[0]
        if redis_proc_info == '':
            console.print('停止成功'.format(timer), style="bold green")
            return False  
    console.print('服务停止失败，请人工检查'.format(timer), style="bold green")


def check_redis_porcess(host, port):
    redis_proc_info = ssh_cli(host, 'ps -ef |grep redis-server |grep :{} |grep -v grep'.format(port))[0]
    if redis_proc_info == '':
        return False  
    else:
        print(redis_proc_info)
        redis_process_num = ssh_cli(host, "ps -ef |grep redis-server |grep :%s |grep -v grep | awk '{print $2}'"%(port))[0].strip()
        redis_kill_cmd = 'kill -9 {};'.format(redis_process_num)
        return(redis_kill_cmd)


def remove_redis(host, port):
    console.print('开始删除主机实例：{0}:{1}'.format(host, port), style="bold green")
    console.print('开始清理实例进程', style="bold green")
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


def install_redis(inst_info):
    def check_redis_proc_exists(host, port):
        console.print('开始检查端口号是否被进程占用', style="bold green")
        while True:
            redis_proc_info =  check_redis_porcess(host, port)
            if redis_proc_info:
                console.print('kill命令为：{0}'.format(redis_proc_info), style="bold red")
                redis_kill_ok = input("\033[5;34m{0}\033[0m".format('请确认kill命令是否正确(yes or no)：'))
                if redis_kill_ok == 'yes':
                    ssh_cli(host, redis_proc_info)
                else:
                    return False  # 取消任务
            else:
                console.print('进程不存在或已经清理！！！！', style="bold green")
                return True

    def check_redis_dir_exists(host, port):
        console.print('开始待检查目录是否存在', style="bold green")
        cmd = 'ls /dbs/redis/ |egrep "^redis{}$" |wc -l'.format(port)
        redis_check_dir_ok = ssh_cli(host, cmd)[0].strip()
        if redis_check_dir_ok == '1':
            redis_rm_ok = input("\033[5;34m{0}\033[0m".format('目录，请确认是否删除目录(yes or no)：'))
            if redis_rm_ok == 'yes':
                ssh_cli(host, 'rm -fr /dbs/redis/redis{}'.format(port))
            else:
                return False  # 取消任务 
        return True


    def make_redis_dir(db_version, host, port):
        redis_package_path = ssh_cli(host, 'find /dbs/versions -maxdepth 1 -name {}* |tail -1'.format(db_version))[0].strip()
        ssh_cli(host, 'mkdir -p /dbs/redis/redis{}'.format(port))
        ssh_cli(host, 'ln -s {0} /dbs/redis/redis{1}/service '.format(redis_package_path, port))
        ssh_cli(host, 'cp /dbs/redis/redis{0}/service/redis.conf /etc/redis{0}.conf'.format(port))
        ssh_cli(host, "sed -i 's/daemonize no/daemonize yes/g' /etc/redis{}.conf ".format(port))
        ssh_cli(host, "sed -i 's/^bind/# bind/g' /etc/redis{}.conf".format(port))
        ssh_cli(host, "sed -i 's/appendonly no/appendonly yes/g' /etc/redis{}.conf ".format(port))
        ssh_cli(host, "sed -i 's/^logfile.*/logfile \/dbs\/redis\/redis{0}\/redis.log/g' /etc/redis{0}.conf ".format(port))
        ssh_cli(host, "sed -i 's/^dir.*/dir \/dbs\/redis\/redis{0}/g' /etc/redis{0}.conf ".format(port))
        ssh_cli(host, "sed -i 's/^pidfile.*/pidfile \/tmp\/redis{0}.pid/g' /etc/redis{0}.conf ".format(port))
        ssh_cli(host, "sed -i 's/^port.*/port {0}/g' /etc/redis{0}.conf ".format(port))
        ssh_cli(host, "sed -i 's/protected-mode yes/protected-mode no/g' /etc/redis{0}.conf ".format(port))


    def run():
        # 获取数据库版本
        norms_db = {'1': 'redis-4', '2': 'redis-5', '3': 'redis-6', '4': 'redis-7'}
        console.print('\n************** 请选择数据库版本 **************', style="bold yellow")
        for k, v in norms_db.items():
            console.print('{0}: {1}'.format(k,v), style="bold white")
        db_version = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认redis-6）：')) or '3' # MySQL版本

        # 获取实例名
        inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))   # 实例名
        dbaas.execute('select count(*) from ins_info where ins_name = "{}";'.format(inst_name))
        inst_name_check = dbaas.fetchall()[0][0]

        # 参数合法性判断
        if db_version not in ('1', '2', '3', '4') or inst_name_check != 0 or inst_name == '':
            console.print('参数不合法或实例名已存在', style="bold red")
            return False
        
        db_v = norms_db[db_version]

        for role_n in range(len(inst_info)):
            id, ip, port = inst_info[role_n]
            if role_n == 0:
                role = 'master'
            elif role_n == 1:
                role = 'slave '
            elif role_n == 2:
                role = 'logger'
            console.print('开始安装：{0}, ip：{1}, port：{2}'.format(role, ip, port), style="bold green")
            if not check_redis_proc_exists(ip, port):
                return False
            if not check_redis_dir_exists(ip, port):
                return False
            make_redis_dir(db_v, ip, port)
            if not start_redis(ip, port):
                return False
            dbaas.execute('update ins_info set used = 1, ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, role_n, db_v, id))
            dbaas.commit()
            if role_n in (1, 2):
                console.print('开始创建主从复制', style="bold green")
                redis_slave_cmd = '/home/redis/versions/redis-7.0.8/bin/redis-cli -h {0} -p {1} slaveof {2} {3}'.format(ip, port, inst_info[0][1], inst_info[0][2])
                ToolsCmd(redis_slave_cmd)
            set_nginx(inst_name)
    run()