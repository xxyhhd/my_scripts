from generic_scripts.gen_class import dbaas, console
from generic_scripts.list_all_insts import list_insts
from mysql_scripts.login_mysql import login_mysql


def get_action():
    console.print('************** 请选择功能 **************', style="bold yellow")
    console.print(' 1：安装实例            2：查看实例列表\n 3：登录实例            4：启动实例\n 5：停止实例            6：手动备份实例\n 7：备库重搭            8：删除实例\n q：退出', style="bold yellow")
    return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))


def login_db():
    console.print('************** 输入实例名 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名（默认dbaas）：')) or 'dbaas'
    inst_info = dbaas.ReadFromMysql('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        login_mysql(inst_info)
    elif 'redis' in inst_info[0][2]:
        pass
    elif 'redis' in inst_info[0][2]:
        pass


def install_db():
    pass


def main():
    while True:
        action = get_action()
        if action == '1':
            install_db()
        if action == '2':
            list_insts()
        if action == '3':
            login_db()
        if action == 'q':
            return False


if __name__ == "__main__":
    main()