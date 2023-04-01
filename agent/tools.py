import paramiko
import subprocess
import os


# python执行Linux命令的方法
def ToolsCmd(command):
    try:
        subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, encoding="utf-8")
        return (subp.stdout.read(), subp.stderr.read())
    except:
        return False


def ssh_cli(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host='127.0.0.1', port=22, user='root', passwd='123456')
    stdint, stdout, stderr = ssh.exec_command(command)
    res = (stdout.read().decode('utf8'), stderr.read().decode('utf8'))
    ssh.close()
    return(res)


# 获取安装包位置
def get_db_package(package_name):
    package = ToolsCmd('ls /dbs/versions/ |grep {} |sort -r |head -1'.format(package_name))
    if package[0] != 0:
        return os.path.join('/dbs/versions/', package[0].rstrip())
    elif package[0] == 0:
        print('很抱歉！暂时没有这个版本的安装包')
        return False
    else:
        return False