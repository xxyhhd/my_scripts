from generic_scripts.tools import ToolsCmd, ssh_cli
from generic_scripts.global_var import logger, console, dbaas
import time
import re
import random
import inspect
import os


def login_pgsql(inst_info):
    norms = {1: 'master', 2: 'slave', 3: 'logger'}
    console.print('************** 请输入实例角色，提示：该实例只有{}个节点 **************'.format(len(inst_info)), style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    inst_role = input("\033[5;34m{0}\033[0m".format('默认登录主库：')) or '1'
    inst_role = int(inst_role) - 1
    if inst_role > len(inst_info) - 1:
        console.print('抱歉，该实例不存在所选角色', style="bold red")
        return False
    os.system('ssh {0} -t "/dbs/pgsql/pgsql{1}/service/bin/psql -U pgsql{1} -p{1} postgres"'.format(inst_info[inst_role][0], inst_info[inst_role][1]))


def start_pgsql(host, port):
    for timer in range(1, 4):
        pgsql_proc_info = ssh_cli(host, 'ps -ef |grep "dbs/pgsql/pgsql{}/data" |grep -v grep'.format(port))[0]
        if pgsql_proc_info == '':
            console.print('第{0}次尝试启动，{1}:{2}'.format(timer, host, port), style="bold green")
            ssh_cli(host, '/dbs/pgsql/pgsql{0}/service/bin/pg_ctl -D /dbs/pgsql/pgsql{0}/data start -l logfile'.format(port), username='pgsql{}'.format(port), password='pass1314')
            time.sleep(30)
        else:
            console.print('服务启动成功'.format(timer), style="bold green")
            return True    
    console.print('服务启动失败，请人工检查'.format(timer), style="bold green")
    return False


def stop_pgsql(host, port):
    for timer in range(1, 4):
        console.print('第{0}次尝试停止，{1}:{2}'.format(timer, host, port), style="bold green")
        ssh_cli(host, '/dbs/pgsql/pgsql{0}/service/bin/pg_ctl -D /dbs/pgsql/pgsql{0}/data stop -l logfile'.format(port), username='pgsql{}'.format(port), password='pass1314')
        time.sleep(30)
        pgsql_proc_info = ssh_cli(host, 'ps -ef |grep "dbs/pgsql/pgsql{}/data" |grep -v grep'.format(port))[0]
        if pgsql_proc_info == '':
            console.print('停止成功'.format(timer), style="bold green")
            return False  
    console.print('服务停止失败，请人工检查'.format(timer), style="bold green")


def check_pgsql_porcess(host, port):
    pgsql_proc_info = ssh_cli(host, 'ps -ef |grep "dbs/pgsql/pgsql{}/data" |grep -v grep'.format(port))[0]
    if pgsql_proc_info == '':
        return False  
    else:
        return True


def remove_pgsql(host, port):
    console.print('开始删除主机实例：{0}:{1}'.format(host, port), style="bold green")
    console.print('开始清理实例进程', style="bold green")
    while True:
        pgsql_proc_info =  check_pgsql_porcess(host, port)
        if pgsql_proc_info:
            stop_pgsql(host, port)
            break
        else:
            console.print('进程不存在或已经清理！！！！', style="bold green")
            break
    console.print('开始清理实例文件', style="bold green")
    ssh_cli(host, 'rm -fr /dbs/pgsql/pgsql{0}'.format(port))
    console.print('开始清理pgsql用户', style="bold green")
    ssh_cli(host, 'userdel -r pgsql{0}'.format(port))



def install_pgsql(inst_info):
    def check_pgsql_proc_exists(host, port):
        console.print('开始检查端口号是否被进程占用', style="bold green")
        while True:
            pgsql_proc_info =  check_pgsql_porcess(host, port)
            if pgsql_proc_info:
                stop_pgsql(host, port)
            else:
                console.print('进程不存在或已经清理！！！！', style="bold green")
                return True


    def check_pgsql_dir_exists(host, port):
        console.print('开始待检查目录是否存在', style="bold green")
        cmd = 'ls /dbs/pgsql/ |egrep "^pgsql{}$" |wc -l'.format(port)
        pgsql_check_dir_ok = ssh_cli(host, cmd)[0].strip()
        if pgsql_check_dir_ok == '1':
            pgsql_rm_ok = input("\033[5;34m{0}\033[0m".format('目录，请确认是否删除目录(yes or no)：'))
            if pgsql_rm_ok == 'yes':
                ssh_cli(host, 'rm -fr /dbs/pgsql/pgsql{}'.format(port))
            else:
                return False  # 取消任务 
        return True


    def make_pgsql_dir(db_version, host, port):
        pgsql_package_path = ssh_cli(host, 'find /dbs/versions -maxdepth 1 -name {}* |tail -1'.format(db_version))[0].strip()
        ssh_cli(host, 'mkdir -p /dbs/pgsql/pgsql{}/archive'.format(port))
        ssh_cli(host, 'useradd pgsql{}'.format(port))
        ssh_cli(host, 'echo pgsql{}:pass1314|chpasswd'.format(port))

        r1 = ssh_cli(host, 'ln -s {0} /dbs/pgsql/pgsql{1}/service '.format(pgsql_package_path, port))
        ssh_cli(host, 'chown -R pgsql{0} /dbs/pgsql/pgsql{0}'.format(port))

    def init_pgsql(host, port):
        console.print('开始初始化pgsql', style="bold green", highlight=True)
        init_result = ssh_cli(host, '/dbs/pgsql/pgsql{0}/service/bin/initdb -D /dbs/pgsql/pgsql{0}/data'.format(port), username='pgsql{}'.format(port), password='pass1314')
        os.system('scp /root/my_scripts/new/db_scripts/tempfiles/postgresql.conf {}:/dbs/pgsql/pgsql{}/data/postgresql.conf'.format(host, port))
        ssh_cli(host, "sed -i 's/xuxy20/{0}/g' /dbs/pgsql/pgsql{0}/data/postgresql.conf".format(port))
        ssh_cli(host, "echo 'host    all             all             0.0.0.0/0            md5' > /dbs/pgsql/pgsql{}/data/pg_hba.conf".format(port))
        ssh_cli(host, "echo 'local   all             all                                  trust' >> /dbs/pgsql/pgsql{}/data/pg_hba.conf".format(port))

        

    def run():
        # 获取数据库版本
        norms_db = {'1': 'postgresql-10', '2': 'postgresql-11', '3': 'postgresql-12', '4': 'postgresql-13', '5': 'postgresql-14', '6': 'postgresql-15'}
        console.print('\n************** 请选择数据库版本 **************', style="bold yellow")
        for k, v in norms_db.items():
            console.print('{0}: {1}'.format(k,v), style="bold yellow")
        db_version = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认pgsql-12）：')) or '3' # pgsql版本


        # 获取实例名
        inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))   # 实例名
        dbaas.execute('select count(*) from ins_info where ins_name = "{}";'.format(inst_name))
        inst_name_check = dbaas.fetchall()[0][0]

        # 参数合法性判断
        if db_version not in ('1', '2', '3', '4', '5', '6') or inst_name_check != 0 or inst_name == '':
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
            if not check_pgsql_proc_exists(ip, port):
                return False
            if not check_pgsql_dir_exists(ip, port):
                return False
            make_pgsql_dir(db_v, ip, port)
            init_pgsql(ip, port)
            time.sleep(30)
            dbaas.execute('update ins_info set used = 1, ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, role_n, db_v, id))
            dbaas.commit()
            if not start_pgsql(ip, port):
                return False

    run()