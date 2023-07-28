from generic_scripts.global_var import dbaas, logger, console
from generic_scripts.tools import ssh_cli
from kvm_scripts.kvm import list_vm, create_vm, remove_vm, login_vm, start_vm, shutdown_vm
from db_scripts.dbs import list_dbs, login_db, install_db, remove_db, start_db, stop_db, info_db
import os
import time


def get_action_main():
    console.print('\n************** 请选择功能 **************', style="bold yellow")
    console.print('{:<15} {:<15}\n{:<17}'.format('1：实例管理' ,'2：主机管理',  'q：退出'), style="bold white")
    return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))



def function_vm():
    def get_action_vm():
        console.print('\n************** 主机管理 **************', style="bold yellow")
        console.print(' 1：查看主机列表         2：登录主机\n 3：启动主机            4：停止\n 5：创建主机            6：删除主机\n q：返回上一层', style="bold white")
        return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))

    def run():
        while True:
            action = get_action_vm()
            if action == '1': # 查
                console.print(list_vm(), style="bold green")
            elif action == '2': # 登录
                login_vm()
            elif action == '3': # 启动
                start_vm()
            elif action == '4': # 停止
                shutdown_vm()
            elif action == '5': # 新建
                create_vm()
            elif action == '6': # 删除
                remove_vm()
            elif action == 'q':
                break
    run()



def function_db():
    def get_action_db():
        console.print('\n************** 实例管理 **************', style="bold yellow")
        console.print(' 1：安装实例            2：查看实例列表\n 3：登录实例            4：查看实例信息\n 5：启动实例            6：停止实例\n 7：备库重搭            8：删除实例\n q：退出\n', style="bold white")
        return (input("\033[5;34m{0}\033[0m".format('\n你的选择：')))

    def run():
        while True:
            action = get_action_db()
            if action == '1': # 新建
                install_db()
            elif action == '2': # 查看实例列表
                list_dbs()
            elif action == '3': # 登录
                login_db()
            elif action == '4': # 查看实例信息
                info_db()
            elif action == '5': # 开启
                start_db()
            elif action == '6': # 停止
                stop_db()
            elif action == '7': # 新建
                pass
            elif action == '8': # 删除
                pass
                remove_db()
            elif action == 'q':
                break
            elif action == '99':
                pass
    run()


def start_ops():
    print('开始启动主机centos7')
    os.system('virsh start centos7')


    print('开始启动dbaas实例')
    os.system('/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysqld_safe --defaults-file=/etc/my3306.cnf &')
    time.sleep(30)
    dbaas.execute('select distinct hostname from ins_info;')
    ips = dbaas.fetchall()
    for ip in ips:
        print('开始启动服务器{}'.format(ip[0]))
        os.system('virsh start {}'.format(ip[0]))

    print('开始启动公众号服务')   
    ssh_cli('centos7', "docker exec  ab25 bash -c '/root/anaconda3/bin/python /date/aaa.py &'")


def main():
    while True:
        action = get_action_main()
        if action == '1':
            function_db()
        elif action == '2':
            function_vm()
        elif action == 'q':
            return False
        elif action == 'r':
            start_ops()

if __name__ == "__main__":
    main()