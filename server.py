import os
import subprocess
import time
from condb import db
import pymysql
from rich.console import Console


console = Console()
mysql = db('192.168.122.102', 'dbaas', 3306)
norms = {1: 'leader', 2: 'follwer', 3: 'logger'}

# python执行Linux命令的方法
def ToolsCmd(command):
    try:
        subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, encoding="utf-8")
        return (subp.stdout.read(), subp.stderr.read())
    except:
        return False


def get_command():
    console.print('\n************** 1. 请选择功能 **************', style="bold yellow")
    console.print(' 1：安装实例            2：查看实例列表\n 3：登录实例            4：启动实例\n 5：停止实例            6：手动备份实例\n 7：备库重搭            8：删除实例\n q：退出', style="bold yellow")
    return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))

# 获取客户想创建的数据库类型和版本
def get_db_info():
    db_versions = {'1': ['1：mysql-5.6', '2：mysql-5.7',  '3：mysql-8.0'], '2': ['1：redis-4.0',
                                                                              '2：redis-5.0',  '3：redis-6.0'], '3': ['1：pgsql-10', '2：pgsql-11',  '3：pgsql-12']}
    try:
        console.print('\n************** 2. 请选择数据库类型 **************\n1：MySQL\n2：Redis\n3：pgsql', style="bold yellow")
        inst_type = input("\033[5;34m{0}\033[0m".format('\n你的选择：'))

        console.print('\n************** 3. 请选择数据库版本 **************', style="bold yellow")
        for version in db_versions[inst_type]:
            console.print(version, style="bold yellow")
        inst_version = input("\033[5;34m{0}\033[0m".format('\n你的选择：'))
        if (inst_type == '1' and inst_version not in ('1', '2', '3')) \
            or (inst_type == '2' and inst_version not in ('1', '2', '3')) \
                or (inst_type == '3' and inst_version not in ('1', '2', '3')) \
        or (inst_type not in ('1', '2', '3')):
            console.print('输入参数不合法\n', style="bold red")
            return False

        console.print('\n************** 4. 请选择数据库规格 **************\n1：单节点\n2：双节点\n3：三节点',style="bold yellow")
        inst_norm = input("\033[5;34m{0}\033[0m".format('\n你的选择：'))
        if inst_norm not in ('1', '2', '3'):
            console.print('规格选择错误\n', style="bold red")
            return False

        console.print('\n************** 5. 请输入实例名 **************', style="bold yellow")
        inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))

        if inst_name == '':
            console.print('实例名不准为空\n', style="bold red")
            return False
        if mysql.ReadFromMysql('select count(*) from ins_info where ins_name = "{0}"'.format(inst_name))[0][0] != 0:
            console.print('实例名重复，请重新输入\n', style="bold red")
            return False
        print('\n')
        # return ('mysql-5.7','实例名','主从版')
        return ((db_versions[inst_type][int(inst_version)-1].split('：')[1], inst_name, inst_norm))
    except:
        console.print('填写参数不合法\n', style="bold red")
        return False


def get_inst_list():
    return (mysql.ReadFromMysql("select ins_name from ins_info where used = '1' and role = '0';"))


def get_ins_info(inst_name):
    return (mysql.ReadFromMysql("select * from ins_info where ins_name = '{0}';".format(inst_name)))


def login_mysql():
    console.print('\n************** 2. 请输入实例名 **************\n', style="bold yellow")
    [print(x[0]) for x in get_inst_list()]
    print('\n')
    inst_name = input("\033[5;34m{0}\033[0m".format('默认登录dbaas实例：')) or 'dbaas'

    console.print('\n************** 3. 请输入实例角色 **************', style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    ins_role = input("\033[5;34m{0}\033[0m".format('默认登录主库：')) or '1'
    ins_info = get_ins_info(inst_name)

    if ins_role not in ('1', '2', '3'):
        console.print('输入参数不合法', style="bold red")
        return False

    elif len(ins_info) == 0:
        console.print('实例不存在', style="bold red")
        return False

    elif (ins_role == '2' or ins_role == '3') and len(ins_info) == 1:
        console.print('该实例为单节点，不存在所选角色', style="bold red")
        return False

    elif ins_role == '3' and len(ins_info) == 2:
        console.print('该实例为双节点，不存在logger角色', style="bold red")
        return False

    for ins in ins_info:
        if int(ins[6]) == int(ins_role) - 1:
            os.system(
                '/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysql -h{0} -P{1} -uroot -p123456'.format(ins[2], ins[3]))
            return True


def copy_to_agent(host):
    os.system(
        'scp -r /root/scripts/agent_new/* {0}:/root/agent_new/ 1> /dev/null'.format(host))


def ass_resource():
    ids = [0,]
    db_info = get_db_info()  # ('mysql-5.7','实例名','主从版') or False
    if db_info is False:
        return False
    conn = pymysql.connect(host='192.168.122.102', port=3306,
                           user='root', passwd='123456', db='dbaas')
    cursor = conn.cursor()
    cursor.execute('set autocommit=0;')
    cursor.execute(
        'select id from ins_info where used = 0 group by ip order by count(ip) desc limit {0} for update;'.format(db_info[2]))
    for x in cursor.fetchall():
        ids.append(x[0])
    cursor.execute("update ins_info set used = 1, ins_name = '{1}' where id in {0};".format(tuple(ids), db_info[0]))
    cursor.execute(
        'select * from ins_info where id in {0};'.format(tuple(ids)))
    print(4)
    host_res = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    num = 1
    for res in host_res:
        console.print('\n开始安装{0}    host：{1}     port：{2}'.format(norms[num], res[2], res[3]), style="bold yellow")
        os.system('scp -r /root/scripts/agent/* {0}:/root/agent/ 1> /dev/null'.format(res[2]))
        os.system("ssh {0} -t '/root/anaconda3/bin/python3 /root/agent/agent.py {1} {2} {3}'".format(res[2], 'install', res[3], db_info[0]))
        mysql.WriteToMysql("update ins_info set ins_name = '{0}', role = {1}, db_v = '{2}' where id = {3};".format(db_info[1], num - 1, db_info[0], res[0]))
        num += 1
        console.rule()


def main():
    while True:
        res = get_command()
        if res == '1':
            ass_resource()
        elif res == '2':
            [print(x[0]) for x in get_inst_list()]
        elif res == '3':
            login_mysql()
        elif res == '4':
            pass
        elif res == 'q':
            print('\n\n')
            return True
        else:
            print('参数不合法，请重新输入！！！！！！')


main()

