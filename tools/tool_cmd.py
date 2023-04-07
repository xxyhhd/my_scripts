import paramiko
import subprocess


# python执行Linux命令的方法
def ToolsCmd(command):
    try:
        subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, encoding="utf-8")
        return (subp.stdout.read(), subp.stderr.read())
    except:
        return False


def ssh_cli(host, command, username='root', password=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=22, username=username, password=password, timeout=3600)
    stdint, stdout, stderr = ssh.exec_command(command)
    res = (stdout.read().decode('utf8'), stderr.read().decode('utf8'))
    ssh.close()
    return(res)


