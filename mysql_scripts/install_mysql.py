from generic_scripts.gen_class import dbaas, console
from tools.tool_cmd import ssh_cli
from mysql_scripts.check_mysql_process import check_mysqld_porcess
from mysql_scripts.start_mysql import start_mysql
import os
import time
import re


def check_proc_exists(host, port):
    console.print('开始检查端口号是否被进程占用', style="bold yellow")
    while True:
        mysql_proc_info =  check_mysqld_porcess(host, port)
        if mysql_proc_info:
            console.print('kill命令为：{0}'.format(mysql_proc_info), style="bold red")
            kill_ok = input("\033[5;34m{0}\033[0m".format('请确认kill命令是否正确(yes or no)：'))
            if kill_ok == 'yes':
                ssh_cli(host, mysql_proc_info)
            else:
                return False  # 取消任务
        else:
            console.print('进程不存在或已经清理！！！！', style="bold yellow")
            return True


def check_dir_exists(host, port):
    console.print('开始待检查目录是否存在', style="bold yellow")
    cmd = 'ls /dbs/mysqls/ |egrep "^mysql{}$" |wc -l'.format(port)
    check_dir_ok = ssh_cli(host, cmd)[0].strip()
    if check_dir_ok == '1':
        rm_ok = input("\033[5;34m{0}\033[0m".format('目录，请确认是否删除目录(yes or no)：'))
        if rm_ok == 'yes':
            ssh_cli(host, 'rm -fr /dbs/mysqls/mysql{}'.format(port))
        else:
            return False  # 取消任务 
    return True


def make_dir(db_version, host, port):
    package_path = ssh_cli(host, 'find /dbs/versions -maxdepth 1 -name {}* |tail -1'.format(db_version))[0].strip()
    ssh_cli(host, 'mkdir -p /dbs/mysqls/mysql%s/{data,binlog,log,undo}'%(port))
    ssh_cli(host, 'touch /dbs/mysqls/mysql{0}/log/mysql-error.log'.format(port))
    ssh_cli(host, 'ln -s {0} /dbs/mysqls/mysql{1}/service'.format(package_path, port))
    ssh_cli(host, 'chown -R mysql.mysql /dbs/mysqls/mysql{0}'.format(port))
    ssh_cli(host, 'chmod -R 755 /dbs/mysqls/mysql{0}'.format(port))
    os.system('scp /root/my_scripts/mysql_scripts/setuser.sql {}:/tmp/setuser.sql'.format(host))
    os.system('scp /root/my_scripts/mysql_scripts/setuser56.sql {}:/tmp/setuser56.sql'.format(host))
    os.system('scp /root/my_scripts/mysql_scripts/mytemp.cnf {}:/etc/my{}.cnf'.format(host, port))
    ssh_cli(host, "sed -i 's/xuxy19/{0}/g' /etc/my{0}.cnf".format(port))
    ssh_cli(host, "sed -i 's/xuxy20/{0}/g' /etc/my{1}.cnf".format(host.split('.')[-1], port))


def init_mysql(host, port, db_v):
    console.print('开始初始化MySQL', style="bold yellow", highlight=True)

    if '5.6' in db_v:
        init_result = ssh_cli(host, '/dbs/mysqls/mysql{0}/service/scripts/mysql_install_db --defaults-file=/etc/my{0}.cnf --basedir=/dbs/mysqls/mysql{0}/service --datadir=/dbs/mysqls/mysql{0}/data --user=mysql'.format(port))
        time.sleep(15)
        for t in range(10):
            a = ssh_cli(host, 'ps -ef |grep mysql_install_db |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip() 
            if a == '0':
                break
            time.sleep(60)
        if  len(re.findall('OK', init_result[0])) == 2:
            console.print('MySQL初始化成功', style="bold green", highlight=True)
            return True
        else:
            return False
    else:
        ssh_cli(host, '/dbs/mysqls/mysql{0}/service/bin/mysqld --defaults-file=/etc/my{0}.cnf --initialize-insecure'.format(port))
        time.sleep(15)
        for t in range(10):
            a =  ssh_cli(host, 'ps -ef |grep initialize |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip() 
            if a == '0':
                break
            time.sleep(30)
        if ssh_cli(host, 'tail -1 /dbs/mysqls/mysql{0}/log/mysql-error.log |grep "empty password" |wc -l'.format(port))[0].rstrip() == '1':
            console.print('MySQL初始化成功', style="bold green", highlight=True)
            return True
    console.print('MySQL初始化失败', style="bold red", highlight=True)
    return False


def init_user(host, port, db_v):
    console.print('初始化账号权限', style="bold yellow", highlight=True)
    if '5.6' in db_v:
        ssh_cli(host, "/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /tmp/setuser56.sql".format(port))
    else:
        ssh_cli(host, "/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /tmp/setuser.sql".format(port))
    console.print('账号初始化成功', style="bold green", highlight=True)


def build_slave(slave_host, slave_port, master_host, master_port, username='backup',passwd='backup'):
    sql = "change master to master_host='{0}',master_port={1},master_user='{2}',master_password='{3}',master_auto_position=1; start slave;".format(master_host, master_port, username, passwd)
    os.system("/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysql -h{0} -P{1} -p123456 -e \"{2}\"".format(slave_host, slave_port, sql))


def install_mysql():
    # 获取数据库版本
    norms_db = {'1': 'mysql-8.0', '2': 'mysql-5.7', '3': 'mysql-5.6'}
    console.print('\n************** 请选择数据库版本 **************', style="bold yellow")
    for k, v in norms_db.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    db_version = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认mysql-8.0）：')) or '1' # MySQL版本

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
    if db_version not in ('1', '2', '3') or inst_norm > 3 or inst_name_check != 0 or inst_name == '':
        console.print('参数不合法或实例名已存在', style="bold red")
        return False

    where = ''
    db_v = norms_db[db_version]
    insts = {}
    for x in range(inst_norm):
        inst_info = dbaas.RWMsql(('select id into @id from ins_info where used = 0 and db_type = "mysql" {} group by ip order by count(ip) desc limit 1 for update;'.format(where), 'update ins_info set used = 1 where id=@id;', 'select id, ip, port from ins_info where id = @id;'))
        id, ip, port = inst_info[1][0]
        if x == 0:
            role = 'master'
        elif x == 1:
            role = 'slave '
        elif x == 2:
            role = 'logger'
        console.print('开始安装：{0}, ip：{1}, port：{2}'.format(role, ip, port), style="bold yellow")
        if not check_proc_exists(ip, port):
            return False
        if not check_dir_exists(ip, port):
            return False
        make_dir(db_v, ip, port)
        if not init_mysql(ip, port, db_v):
            return False
        if not start_mysql(ip, port):
            return False
        init_user(ip, port, db_v)
        insts[x] = '{}:{}'.format(ip, port)
        # where 下一次分配资源过滤已分配的主机
        where = where + 'and ip !="{0}" '.format(ip) 
        dbaas.WriteToMysql('update ins_info set ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, x, db_v, id))

    console.print('开始搭建复制关系', style="bold yellow")    
    if len(insts) == 1:
        return True
    elif len(insts) == 2:
        build_slave(insts.get(1).split(':')[0], insts.get(1).split(':')[1], insts.get(0).split(':')[0], insts.get(0).split(':')[1])
        build_slave(insts.get(0).split(':')[0], insts.get(0).split(':')[1], insts.get(1).split(':')[0], insts.get(1).split(':')[1])
        return True
    elif len(insts) == 3:
        build_slave(insts.get(1).split(':')[0], insts.get(1).split(':')[1], insts.get(0).split(':')[0], insts.get(0).split(':')[1])
        build_slave(insts.get(0).split(':')[0], insts.get(0).split(':')[1], insts.get(1).split(':')[0], insts.get(1).split(':')[1])
        build_slave(insts.get(2).split(':')[0], insts.get(2).split(':')[1], insts.get(0).split(':')[0], insts.get(0).split(':')[1])      
        return True  


