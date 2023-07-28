from generic_scripts.tools import ToolsCmd, ssh_cli
from generic_scripts.global_var import logger, console, dbaas
import time
import random
import os


def allocate_ip():
    while True:
        ip = '192.168.122.'+str(random.randint(100,200))
        grep_ip_cmd = 'grep {} /etc/host'
        if ToolsCmd(grep_ip_cmd)[0] == '':
            return ip


def list_vm():
    return (ToolsCmd('virsh list --all')[0])


def login_vm():
    vm_name = input("\033[5;34m{0}\033[0m".format('\n请输入待登录主机主机名：'))
    if ToolsCmd("virsh list --all |grep running |grep ' {} '".format(vm_name))[0] == '' or vm_name == '':
        console.print('\n主机名不存在或主机未运行', style="bold red")
        return False
    os.system('ssh -t {}'.format(vm_name))


def start_vm():
    vm_name = input("\033[5;34m{0}\033[0m".format('\n请输入待登录主机主机名：'))
    if ToolsCmd("virsh list --all |grep 关闭 |grep ' {} '".format(vm_name))[0] == '' or vm_name == '':
        console.print('\n主机名不存在或主机已启动', style="bold red")
        return False
    os.system('virsh start {}'.format(vm_name))
    console.print('\n主机已启动', style="bold green")



def shutdown_vm():
    vm_name = input("\033[5;34m{0}\033[0m".format('\n请输入待登录主机主机名：'))
    if ToolsCmd("virsh list --all |grep running |grep ' {} '".format(vm_name))[0] == '' or vm_name == '':
        console.print('\n主机名不存在或主机已关闭', style="bold red")
        return False
    os.system('virsh shutdown {}'.format(vm_name))
    console.print('\n主机已停止', style="bold green")




def create_vm():
    step = '''
    1. 使用centos7-demo模版机克隆新的vm
    2. 启动新的vm，并登录修改主机名和IP，然后重启机器
    3. 验证
    '''
    vm_new = input("\033[5;34m{0}\033[0m".format('\n请输入主机名：'))
    vm_old = input("\033[5;34m{0}\033[0m".format('\n请输入模版机主机名：')) or 'centos7-demo'
    if ToolsCmd("virsh list --all |grep ' {} '".format(vm_new))[0] != '' or vm_new == '':
        console.print('\n已存在同名主机', style="bold red")
        return False

    if ToolsCmd("virsh list --all |grep 关闭 |grep ' {} '".format(vm_old))[0] == '' or vm_old == '':
        console.print('\n模版机不存在或已打开', style="bold red")
        return False

    ip = allocate_ip()
    clone_cmd = 'virt-clone -o {1} -n {0} -f /home/kvms/{0}.qcow2'.format(vm_new, vm_old)
    start_vm_cmd = 'virsh start {}'.format(vm_new)
    reboot_vm_cmd = 'virsh reboot {}'.format(vm_new)
    set_hostname_cmd = 'hostnamectl set-hostname {}'.format(vm_new)
    set_ip_cmd = "sed -i 's/192.168.122.10/{}/' /etc/sysconfig/network-scripts/ifcfg-ens3".format(ip)
    set_dns_cmd = 'echo {} {} >> /etc/hosts'.format(ip, vm_new)
    console.print('\n开始克隆新主机', style="bold green")
    res_clone = ToolsCmd(clone_cmd)
    if res_clone[1] !='':
        console.print('\n克隆失败！！！！！！！', style="bold red")
        return False
    time.sleep(10)
    console.print('\n克隆完成，等待开启虚拟机并完成必要配置', style="bold green")
    ToolsCmd(start_vm_cmd)
    time.sleep(120)
    ssh_cli(vm_old, set_hostname_cmd)
    time.sleep(1)
    ssh_cli(vm_old, set_ip_cmd)
    ToolsCmd(set_dns_cmd)
    ToolsCmd(reboot_vm_cmd)
    console.print('\n主机创建完成', style="bold green")



def remove_vm():
    step = '''
    1. 强制停止vm
    2. 取消vm定义
    3. 删除无用文件
    4. 验证
    '''
    vm_name = input("\033[5;34m{0}\033[0m".format('\n请输入待删除主机主机名：'))
    if ToolsCmd("virsh list --all |grep ' {} '".format(vm_name))[0] == '' or vm_name == '':
        console.print('\n主机名不存在', style="bold red")
        return False
    
    console.print('\n强制停止主机', style="bold green")
    destory_cmd = 'virsh destroy {}'.format(vm_name)
    undefine_cmd = 'virsh undefine {}'.format(vm_name)
    console.print('\n开始删除遗留文件', style="bold green")
    rm_qcow2_cmd = 'rm -fr /home/kvms/{}.qcow2'.format(vm_name)
    rm_xml_cmd = 'rm -fr /etc/libvirt/qemu/{}.xml'.format(vm_name)
    rm_log_cmd = 'rm -fr /var/log/libvirt/qemu/{}.log*'.format(vm_name)
    remove_dns_cmd = "sed -i '/.* {}$/d' /etc/hosts".format(vm_name)
    ToolsCmd(destory_cmd)
    ToolsCmd(undefine_cmd)
    ToolsCmd(rm_qcow2_cmd)
    ToolsCmd(rm_xml_cmd)
    ToolsCmd(rm_log_cmd)
    ToolsCmd(remove_dns_cmd)