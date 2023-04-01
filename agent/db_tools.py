# import os
# import time
# from datetime import datetime
# from tools import ToolsCmd, get_db_package
from install_mysql.a_check_process import check_proc
from install_mysql.b_check_dir import check_dir
from install_mysql.c_mkdir import mkdir
from install_mysql.d_rmdir import rm_dir
from install_mysql.e_ln_to_pachage import ln
from install_mysql.f_change_file_owner import chang_user
from install_mysql.g_build_cnf import cnf
from install_mysql.h_init_mysql import init_mysql
from install_mysql.i_start_mysql import start_mysql
from install_mysql.j_init_user import init_user


def install_mysql(port, db_v):
    check_proc(port)
    if check_dir(port) is False:
        rm_dir(port)
    mkdir(port)
    ln(port, db_v)
    chang_user(port)
    cnf(port)
    init_mysql(port, db_v)
    start_mysql(port)
    init_user(port, db_v)



# def check_mysql_process(port):
#     return(ToolsCmd('ps -ef |grep mysqld |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip())


# def start_mysql(port):
#     print('开始起服务')
#     os.system('/dbs/mysqls/mysql{0}/service/bin/mysqld_safe --defaults-file=/etc/my{0}.cnf & '.format(port))
#     time.sleep(20)
#     if check_mysql_process(port) == '2':
#         print('服务启动成功')
#         return True
#     return False


# def stop_mysql(port):
#     print('开始停止服务')
#     os.system('/dbs/mysqls/mysql{0}/service/bin/mysqladmin -h127.0.0.1 -P{0} -p123456 shutdown'.format(port))
#     time.sleep(20)
#     if check_mysql_process(port) == '0':
#         print('服务停止成功')
#         return True
#     return False


# def install_mysql(package, port):
#     print('开始创建工作目录等前置工作')
#     ToolsCmd('mkdir -p /dbs/mysqls/mysql{0}/binlog'.format(port))
#     ToolsCmd('mkdir -p /dbs/mysqls/mysql{0}/data'.format(port))
#     ToolsCmd('mkdir -p /dbs/mysqls/mysql{0}/log'.format(port))
#     ToolsCmd('mkdir -p /dbs/mysqls/mysql{0}/undo'.format(port))
#     ToolsCmd('touch /dbs/mysqls/mysql{0}/log/mysql-error.log'.format(port))
#     ToolsCmd('ln -s {0} /dbs/mysqls/mysql{1}/service'.format(package, port))
#     ToolsCmd('chown -R mysql.mysql /dbs/mysqls/')
#     ToolsCmd('chmod -R 755 /dbs/mysqls/')
#     ToolsCmd('cp -f /etc/mytemp.cnf /etc/my{0}.cnf'.format(port))
#     ToolsCmd("sed -i 's/xuxy19/{0}/g' /etc/my{0}.cnf".format(port))
#     print('开始初始化安装MySQL')
#     ToolsCmd('/dbs/mysqls/mysql{0}/service/bin/mysqld --defaults-file=/etc/my{0}.cnf --initialize-insecure'.format(port))
#     time.sleep(15)
#     for t in range(10):
#         a =  ToolsCmd('ps -ef |grep initialize |grep my{0} |grep -v grep |wc -l'.format(port))[0].rstrip() 
#         if a == '0':
#             break
#         time.sleep(30)
#     time.sleep(10)
#     print('初始化安装完成')
#     start_mysql(port)
#     print('开始初始化账号权限')
#     ToolsCmd("/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /root/agent/setuser.sql".format(port))
#     print('安装完成')
#     return True


# def install_redis():
#     pass


# def install_pgsql():
#     pass


# def install_db(port, db_v):
#     package = get_db_package(db_v)
#     if package is False:
#         return False
#     if 'mysql' in db_v:
#         print('开始安装{}'.format(db_v))
#         install_mysql(package, port)
#     elif 'redis' in db_v:
#         print('开始安装{}'.format(db_v))
#     elif 'pgsql' in db_v:
#         print('开始安装{}'.format(db_v))
#     return True


# def remove_db(port, db_v):
#     if 'mysql' in db_v :
#         print('开始停服务')
#         stop_mysql(port)
#         print('删除工作目录')
#         ToolsCmd('rm -fr /dbs/mysqls/mysql{0}'.format(port))
#     pass