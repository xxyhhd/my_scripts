from generic_scripts.gen_class import dbaas, console
from generic_scripts.list_all_insts import list_insts
from mysql_scripts.login_mysql import login_mysql
from mysql_scripts.install_mysql import install_mysql
from mysql_scripts.remove_inst import remove_mysql
from mysql_scripts.full_backup_mysql import full_backup_mysql
from mysql_scripts.stop_mysql import stop_mysql
from mysql_scripts.start_mysql import start_mysql
from redis_scripts.install_redis import install_redis
from redis_scripts.login_redis import login_redis
from redis_scripts.start_redis import start_redis
from redis_scripts.stop_redis import stop_redis
from redis_scripts.remove_redis import remove_redis
from pgsql_scripts.install_pgsql import install_pgsql
from pgsql_scripts.login_pgsql import login_pgsql
from pgsql_scripts.start_pgsql import start_pgsql
from pgsql_scripts.stop_pgsql import stop_pgsql
from pgsql_scripts.remove_pgsql import remove_pgsql
from start_ops import start_ops
# from kvm_scripts.kvm import create_vm, remove_vm


def get_action_old():
    console.print('\n************** 请选择功能 **************', style="bold yellow")
    console.print(' 1：安装实例            2：查看实例列表\n 3：登录实例            4：启动实例\n 5：停止实例            6：手动备份实例\n 7：备库重搭            8：删除实例\n q：退出', style="bold yellow")
    return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))


def get_action():
    console.print('\n************** 请选择功能 **************', style="bold yellow")
    console.print(' 1：安装实例            2：查看实例列表\n 3：登录实例            4：启动实例\n 5：停止实例            6：手动备份实例\n 7：备库重搭            8：删除实例\n q：退出\n-------------------------------------\n a：创建vm              b：删除vm\n r：环境恢复', style="bold yellow")
    return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))







def login_db():
    console.print('\n************** 输入实例名 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名（默认登录dbaas）：')) or 'dbaas'
    inst_info = dbaas.ReadFromMysql('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        login_mysql(inst_info)
    elif 'redis' in inst_info[0][2]:
        login_redis(inst_info)
    elif 'postgres' in inst_info[0][2]:
        login_pgsql(inst_info)


def install_db():
    norms = {1: 'MySQL', 2: 'Redis', 3: 'PgSql'}
    console.print('\n************** 请选择数据库类型 **************', style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    db_type = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认MySQL）')) or '1'
    if db_type == '1':
        install_mysql()
    elif db_type == '2':
        install_redis()
    elif db_type == '3':
        install_pgsql()
    else:
        console.print('很抱歉，参数不合法！！！', style="bold red")


def remove_db():
    console.print('\n************** 开始删除实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入待删除的实例名'))
    inst_info = dbaas.ReadFromMysql('select ip, port, db_type from ins_info where ins_name = "{}"'.format(inst_name))
    if len(inst_info) > 0:
        for inst in inst_info:
            if inst[2] == 'mysql':
                remove_mysql(inst[0], inst[1])
            if inst[2] == 'redis':
                remove_redis(inst[0], inst[1])
            elif inst[2] == 'postgresql':
                remove_pgsql(inst[0], inst[1])
        dbaas.WriteToMysql("update ins_info set used=0, ins_name=NULL, role=NULL,db_v=NULL where ins_name='{}';".format(inst_name))
        console.print('实例已删除', style="bold green")
    else:
        console.print('该实例不存在！！！！', style="bold red")       


def backup_db():
    console.print('\n************** 开始临时备份实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))
    inst_info = dbaas.ReadFromMysql('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        full_backup_mysql(inst_info)
    elif 'redis' in inst_info[0][2]:
        pass
    elif 'pgsql' in inst_info[0][2]:
        pass


def stop_db():
    console.print('\n************** 开始停止实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))
    inst_info = dbaas.ReadFromMysql('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        for inst in inst_info:
            stop_mysql(inst[0], inst[1])
    elif 'redis' in inst_info[0][2]:
        for inst in inst_info:
            stop_redis(inst[0], inst[1])
    elif 'postgres' in inst_info[0][2]:
        for inst in inst_info:
            stop_pgsql(inst[0], inst[1])


def start_db():
    console.print('\n************** 开始启动实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))
    inst_info = dbaas.ReadFromMysql('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        for inst in inst_info:
            start_mysql(inst[0], inst[1])
    elif 'redis' in inst_info[0][2]:
        for inst in inst_info:
            start_redis(inst[0], inst[1])
    elif 'postgres' in inst_info[0][2]:
        for inst in inst_info:
            start_pgsql(inst[0], inst[1])


def main():
    while True:
        action = get_action()
        if action == '1':
            install_db()
        if action == '2':
            list_insts()
        if action == '3':
            login_db()
        if action == '4':
            start_db()
        if action == '5':
            stop_db()
        if action == '6':
            backup_db()
        if action == '8':
            remove_db()
        if action == 'q':
            return False
        if action == 'r':
            start_ops()

if __name__ == "__main__":
    main()
