from generic_scripts.gen_class import console
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
