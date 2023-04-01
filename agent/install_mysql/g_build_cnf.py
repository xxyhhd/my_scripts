from tools import ToolsCmd
from rich.console import Console


console = Console()

def cnf(port):
    console.print('\n6-开始创建并修改配置文件', style="bold yellow")
    ToolsCmd('cp -f /etc/mytemp.cnf /etc/my{0}.cnf'.format(port))
    ToolsCmd("sed -i 's/xuxy19/{0}/g' /etc/my{0}.cnf".format(port))
    console.print('修改配置文件成功', style="bold green")
    return True