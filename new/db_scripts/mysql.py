from generic_scripts.tools import ToolsCmd, ssh_cli
from generic_scripts.global_var import logger, console, dbaas
from nginx import set_nginx
import time
import re
import random
import inspect
import os


def login_mysql(inst_info):
    norms = {1: 'master', 2: 'slave', 3: 'logger'}
    console.print('************** 请输入实例角色，提示：该实例只有{}个节点 **************'.format(len(inst_info)), style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    inst_role = input("\033[5;34m{0}\033[0m".format('默认登录主库：')) or '1'
    inst_role = int(inst_role) - 1
    if inst_role > len(inst_info) - 1:
        console.print('抱歉，该实例不存在所选角色', style="bold red")
        return False
    os.system('/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysql -h{0} -P{1} -uroot -p123456'.format(inst_info[inst_role][0], inst_info[inst_role][1]))


def start_mysql(host, port):
    for timer in range(1, 4):
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep mysqld |grep {} |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('第{0}次尝试启动，{1}:{2}'.format(timer, host, port), style="bold green")
            os.system('ssh {0} -t /dbs/mysqls/mysql{1}/service/bin/mysqld_safe --defaults-file=/etc/my{1}.cnf & '.format(host, port))
            time.sleep(30)
        else:
            console.print('服务启动成功'.format(timer), style="bold green")
            return True    
    console.print('服务启动失败，请人工检查'.format(timer), style="bold green")
    return False


def stop_mysql(host, port):
    for timer in range(1, 4):
        console.print('第{0}次尝试停止，{1}:{2}'.format(timer, host, port), style="bold green")
        cmd_stop = '/dbs/mysqls/mysql{0}/service/bin/mysqladmin -uroot -P{0} -p123456 -h127.0.0.1 shutdown'.format(port)
        ssh_cli(host, cmd_stop)
        time.sleep(30)
        mysql_proc_info = ssh_cli(host, 'ps -ef |grep mysqld |grep {} |grep -v grep'.format(port))[0]
        if mysql_proc_info == '':
            console.print('停止成功'.format(timer), style="bold green")
            return False  
    console.print('服务停止失败，请人工检查'.format(timer), style="bold green")


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
    

def install_mysql(inst_info):    
    def check_proc_exists(host, port):
        console.print('开始检查端口号是否被进程占用', style="bold green")
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
                console.print('进程不存在或已经清理！！！！', style="bold green")
                return True

    def check_dir_exists(host, port):
        console.print('开始待检查目录是否存在', style="bold green")
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
        ToolsCmd('scp /root/my_scripts/new/db_scripts/tempfiles/setuser.sql {}:/tmp/setuser.sql'.format(host))
        ToolsCmd('scp /root/my_scripts/new/db_scripts/tempfiles/setuser56.sql {}:/tmp/setuser56.sql'.format(host))
        ToolsCmd('scp /root/my_scripts/new/db_scripts/tempfiles/mytemp.cnf {}:/etc/my{}.cnf'.format(host, port))
        ssh_cli(host, "sed -i 's/xuxy19/{0}/g' /etc/my{0}.cnf".format(port))
        ssh_cli(host, "sed -i 's/xuxy20/{0}/g' /etc/my{1}.cnf".format('1'+host.split('.')[-1], port))
        

    def init_mysql(host, port, db_v):
        console.print('开始初始化MySQL', style="bold green", highlight=True)

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
        console.print('初始化账号权限', style="bold green", highlight=True)
        if '5.6' in db_v:
            ssh_cli(host, "/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /tmp/setuser56.sql".format(port))
        else:
            ssh_cli(host, "/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /tmp/setuser.sql".format(port))
        console.print('账号初始化成功', style="bold green", highlight=True)


    def build_slave(slave_host, slave_port, master_host, master_port, username='backup',passwd='backup'):
        sql = "change master to master_host='{0}',master_port={1},master_user='{2}',master_password='{3}',master_auto_position=1; start slave;".format(master_host, master_port, username, passwd)
        ToolsCmd("/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysql -h{0} -P{1} -p123456 -e \"{2}\"".format(slave_host, slave_port, sql))


    def run():
        # 获取数据库版本
        norms_db = {'1': 'mysql-8.0', '2': 'mysql-5.7', '3': 'mysql-5.6'}
        console.print('\n************** 请选择数据库版本 **************', style="bold yellow")
        for k, v in norms_db.items():
            console.print('{0}: {1}'.format(k,v), style="bold white")
        db_version = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认mysql-8.0）：')) or '1' # MySQL版本

        # 获取实例名
        inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))   # 实例名
        dbaas.execute('select count(*) from ins_info where ins_name = "{}";'.format(inst_name))
        inst_name_check = dbaas.fetchall()[0][0]

        # 参数合法性判断
        if db_version not in ('1', '2', '3')  or inst_name_check != 0 or inst_name == '':
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
            dbaas.execute('update ins_info set used = 1, ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, role_n, db_v, id))
            dbaas.commit()

        if len(inst_info) == 1:
            return True
        elif len(inst_info) == 2:
            console.print('开始搭建复制关系', style="bold green")    
            build_slave(inst_info[1][1], inst_info[1][2], inst_info[0][1], inst_info[0][2])
            build_slave(inst_info[0][1], inst_info[0][2], inst_info[1][1], inst_info[1][2])
        elif len(inst_info) == 3:
            console.print('开始搭建复制关系', style="bold green")    
            build_slave(inst_info[1][1], inst_info[1][2], inst_info[0][1], inst_info[0][2])
            build_slave(inst_info[0][1], inst_info[0][2], inst_info[1][1], inst_info[1][2])
            build_slave(inst_info[2][1], inst_info[2][2], inst_info[0][1], inst_info[0][2])      
        console.print('开始配置Nginx反向代理', style="bold green")    
        set_nginx(inst_name)
    run()


def remove_mysql(host, port):
    console.print('开始删除主机实例：{0}:{1}'.format(host, port), style="bold green")
    console.print('开始清理实例进程', style="bold green")
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
            console.print('进程不存在或已经清理！！！！', style="bold green")
            break
    console.print('开始清理实例文件', style="bold green")
    ssh_cli(host, 'rm -fr /dbs/mysqls/mysql{0}'.format(port))