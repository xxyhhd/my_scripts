import os
from generic_scripts.gen_class import dbaas
from time import sleep
from tools.tool_cmd import ssh_cli


def start_ops():
    print('开始启动主机centos7')
    os.system('virsh start centos7')


    print('开始启动dbaas实例')
    os.system('/home/mysqls/versions/mysql-8.0.28-el7-x86_64/bin/mysqld_safe --defaults-file=/etc/my3306.cnf &')
    sleep(10)
    ips = dbaas.ReadFromMysql('select distinct ip from ins_info;')
    for ip in ips:
        print('开始启动服务器{}'.format(ip[0]))
        os.system('virsh start {}'.format(ip[0]))

    print('开始启动公众号服务')   
    ssh_cli('centos7', "docker exec  ab25 bash -c '/root/anaconda3/bin/python /date/aaa.py &'")