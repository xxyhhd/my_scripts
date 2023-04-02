from generic_scripts.gen_class import console
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
