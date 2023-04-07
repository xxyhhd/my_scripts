from generic_scripts.gen_class import dbaas, console
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


# def build_slave(slave_host, slave_port, master_host, master_port, username='backup',passwd='backup'):
#     sql = "change master to master_host='{0}',master_port={1},master_user='{2}',master_password='{3}',master_auto_position=1; start slave;".format(master_host, master_port, username, passwd)
#     os.system("/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysql -h{0} -P{1} -p123456 -e \"{2}\"".format(slave_host, slave_port, sql))


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
    inst_norm = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认双节点）：')) or '2'   # 实例规格
    inst_norm = int(inst_norm)

    # 获取实例名
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))   # 实例名
    inst_name_check = dbaas.ReadFromMysql('select count(*) from ins_info where ins_name = "{}";'.format(inst_name))[0][0]

    # 参数合法性判断
    if db_version not in ('1', '2', '3', '4') or inst_norm > 3 or inst_name_check != 0 or inst_name == '':
        console.print('参数不合法或实例名已存在', style="bold red")
        return False

    where = ''
    db_v = norms_db[db_version]
    insts = {}
    for x in range(inst_norm):
        inst_info = dbaas.RWMsql(('select id into @id from ins_info where used = 0 and db_type = "redis" {} group by ip order by count(ip) desc limit 1 for update;'.format(where), 'update ins_info set used = 1 where id=@id;', 'select id, ip, port from ins_info where id = @id;'))
        id, ip, port = inst_info[1][0]
        if x == 0:
            role = 'master'
        elif x == 1:
            role = 'slave '
        elif x == 2:
            role = 'logger'
        console.print('开始安装：{0}, ip：{1}, port：{2}'.format(role, ip, port), style="bold yellow")
        if not check_redis_proc_exists(ip, port):
            return False
        if not check_redis_dir_exists(ip, port):
            return False
        make_redis_dir(db_v, ip, port)
        start_redis(ip, port)
        insts[x] = '{}:{}'.format(ip, port)
        # where 下一次分配资源过滤已分配的主机
        where = where + 'and ip !="{0}" '.format(ip) 
        dbaas.WriteToMysql('update ins_info set ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, x, db_v, id))

    # console.print('开始搭建复制关系', style="bold yellow")    
    # if len(insts) == 1:
    #     return True
    # elif len(insts) == 2:
    #     build_slave(insts.get(1).split(':')[0], insts.get(1).split(':')[1], insts.get(0).split(':')[0], insts.get(0).split(':')[1])
    #     build_slave(insts.get(0).split(':')[0], insts.get(0).split(':')[1], insts.get(1).split(':')[0], insts.get(1).split(':')[1])
    #     return True
    # elif len(insts) == 3:
    #     build_slave(insts.get(1).split(':')[0], insts.get(1).split(':')[1], insts.get(0).split(':')[0], insts.get(0).split(':')[1])
    #     build_slave(insts.get(0).split(':')[0], insts.get(0).split(':')[1], insts.get(1).split(':')[0], insts.get(1).split(':')[1])
    #     build_slave(insts.get(2).split(':')[0], insts.get(2).split(':')[1], insts.get(0).split(':')[0], insts.get(0).split(':')[1])      
    #     return True  

