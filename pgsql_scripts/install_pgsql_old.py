from generic_scripts.gen_class import dbaas, console
from generic_scripts.ass_resource import ass_resource
from tools.tool_cmd import ssh_cli
from pgsql_scripts.check_pgsql_process import check_pgsql_porcess
from pgsql_scripts.start_pgsql import start_pgsql
import time


def test()



# def check_pgsql_proc_exists(host, port):
#     console.print('开始检查端口号是否被进程占用', style="bold yellow")
#     while True:
#         pgsql_proc_info =  check_pgsql_porcess(host, port)
#         if pgsql_proc_info:
#             console.print('kill命令为：{0}'.format(pgsql_proc_info), style="bold red")
#             pgsql_kill_ok = input("\033[5;34m{0}\033[0m".format('请确认kill命令是否正确(yes or no)：'))
#             if pgsql_kill_ok == 'yes':
#                 ssh_cli(host, pgsql_proc_info)
#             else:
#                 return False  # 取消任务
#         else:
#             console.print('进程不存在或已经清理！！！！', style="bold yellow")
#             return True


# def check_pgsql_dir_exists(host, port):
#     console.print('开始待检查目录是否存在', style="bold yellow")
#     cmd = 'ls /dbs/pgsql/ |egrep "^pgsql{}$" |wc -l'.format(port)
#     pgsql_check_dir_ok = ssh_cli(host, cmd)[0].strip()
#     if pgsql_check_dir_ok == '1':
#         pgsql_rm_ok = input("\033[5;34m{0}\033[0m".format('目录，请确认是否删除目录(yes or no)：'))
#         if pgsql_rm_ok == 'yes':
#             ssh_cli(host, 'rm -fr /dbs/pgsql/pgsql{}'.format(port))
#         else:
#             return False  # 取消任务 
#     return True


# def make_pgsql_dir(db_version, host, port):
#     pgsql_package_path = ssh_cli(host, 'find /dbs/versions -maxdepth 1 -name {}* |tail -1'.format(db_version))[0].strip()
#     ssh_cli(host, 'mkdir -p /dbs/pgsql/pgsql{}'.format(port))
#     ssh_cli(host, 'useradd pgsql{}'.format(port))
#     ssh_cli(host, 'echo pgsql{}:pass1314|chpasswd'.format(port))
#     ssh_cli(host, 'chown pgsql{0} /dbs/pgsql/pgsql{0}'.format(port))
#     ssh_cli(host, 'ln -s {0} /dbs/pgsql/pgsql{1}/service '.format(pgsql_package_path, port), 'pgsql{}'.format(port), 'pass1314')
#     ssh_cli(host, "sed -i 's/#listen_addresses = 'localhost'/listen_addresses = '*'/g' /dbs/pgsql/pgsql{}/data/postgresql.conf".format(port), username='pgsql{}'.format(port), password='pass1314')
#     ssh_cli(host, "sed -i 's/#port = 5432 /port = {0} /g' /dbs/pgsql/pgsql{0}/data/postgresql.conf".format(port), username='pgsql{}'.format(port), password='pass1314')

#     #ssh_cli(host, "sed -i 's/#archive_mode = off/archive_mode = on/g' /dbs/pgsql/pgsql{0}/data/postgresql.conf".format(port), username='pgsql{}'.format(port), password='pass1314')





# def init_pgsql(host, port):
#     console.print('开始初始化pgsql', style="bold yellow", highlight=True)
#     init_result = ssh_cli(host, '/dbs/pgsql/pgsql{0}/service/bin/initdb -D /dbs/pgsql/pgsql{0}/data'.format(port), username='pgsql{}'.format(port), password='pass1314')


# def install_pgsql():
#     # 获取数据库版本
#     norms_db = {'1': 'postgresql-10', '2': 'postgresql-11', '3': 'postgresql-12', '4': 'postgresql-13', '5': 'postgresql-14', '6': 'postgresql-15'}
#     console.print('\n************** 请选择数据库版本 **************', style="bold yellow")
#     for k, v in norms_db.items():
#         console.print('{0}: {1}'.format(k,v), style="bold yellow")
#     db_version = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认pgsql-12）：')) or '3' # pgsql版本

#     # 获取实例规格
#     norms_norm = {1: '单节点', 2: '双节点', 3: '三节点'}
#     console.print('\n************** 请选择实例规格 **************', style="bold yellow")
#     for k, v in norms_norm.items():
#         console.print('{0}: {1}'.format(k,v), style="bold yellow")
#     inst_num = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认双节点）：')) or '2'   # 实例规格
#     inst_num = int(inst_num)

#     # 获取实例名
#     inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))   # 实例名
#     inst_name_check = dbaas.ReadFromMysql('select count(*) from ins_info where ins_name = "{}";'.format(inst_name))[0][0]

#     # 参数合法性判断
#     if db_version not in ('1', '2', '3', '4', '5', '6') or inst_num > 3 or inst_name_check != 0 or inst_name == '':
#         console.print('参数不合法或实例名已存在', style="bold red")
#         return False

#     db_v = norms_db[db_version]
#     print(db_v.split('-')[0])
#     inst_resource = ass_resource(inst_num, db_v.split('-')[0])
#     if not inst_resource:
#         return False
#     for resource in inst_resource:
#         id, ip, port = inst_resource[resource]
#         if resource == 0:
#             role = 'master'
#         elif resource == 1:
#             role = 'slave '
#         elif resource == 2:
#             role = 'logger'
#         console.print('开始安装：{0}, ip：{1}, port：{2}'.format(role, ip, port), style="bold yellow")
#         if not check_pgsql_proc_exists(ip, port):
#             return False
#         if not check_pgsql_dir_exists(ip, port):
#             return False
#         make_pgsql_dir(db_v, ip, port)
#         init_pgsql(ip, port)
#         start_pgsql(ip, port)
        # dbaas.WriteToMysql('update ins_info set ins_name = "{0}", role = {1}, db_v = "{2}" where id={3};'.format(inst_name, resource, db_v, id))

