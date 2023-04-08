from generic_scripts.gen_class import dbaas, console
from generic_scripts.ass_resource import ass_resource
from tools.tool_cmd import ssh_cli
from redis_scripts.check_redis_process import check_redis_porcess
from redis_scripts.start_redis import start_redis


def check_redis_proc_exists(host, port):
    console.print('开始检查端口号是否被进程占用', style="bold yellow")
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
            console.print('进程不存在或已经清理！！！！', style="bold yellow")
            return True


def check_redis_dir_exists(host, port):
    console.print('开始待检查目录是否存在', style="bold yellow")
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


def install_redis():
    # 获取数据库版本
    norms_db = {'1': 'redis-4', '2': 'redis-5', '3': 'redis-6', '4': 'redis-7'}
    console.print('\n************** 请选择数据库版本 **************', style="bold yellow")
    for k, v in norms_db.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    db_version = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认redis-6）：')) or '3' # MySQL版本

    # 获取实例规格
    norms_norm = {1: '单节点', 2: '双节点', 3: '三节点'}
    console.print('\n************** 请选择实例规格 **************', style="bold yellow")
    for k, v in norms_norm.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    inst_num = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认双节点）：')) or '2'   # 实例规格
    inst_num = int(inst_num)

    # 获取实例名
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))   # 实例名
    inst_name_check = dbaas.ReadFromMysql('select count(*) from ins_info where ins_name = "{}";'.format(inst_name))[0][0]

    # 参数合法性判断
    if db_version not in ('1', '2', '3', '4') or inst_num > 3 or inst_name_check != 0 or inst_name == '':
        console.print('参数不合法或实例名已存在', style="bold red")
        return False
    
    db_v = norms_db[db_version]
    print(db_v.split('-')[0])
    inst_resource = ass_resource(inst_num, db_v.split('-')[0])
    if not inst_resource:
        return False
    for resource in inst_resource:
        id, ip, port = inst_resource[resource]
        if resource == 0:
            role = 'master'
        elif resource == 1:
            role = 'slave '
        elif resource == 2:
            role = 'logger'
        console.print('开始安装：{0}, ip：{1}, port：{2}'.format(role, ip, port), style="bold yellow")
        if not check_redis_proc_exists(ip, port):
            return False
        if not check_redis_dir_exists(ip, port):
            return False
        make_redis_dir(db_v, ip, port)
        start_redis(ip, port)
        dbaas.WriteToMysql('update ins_info set ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, resource, db_v, id))



 


