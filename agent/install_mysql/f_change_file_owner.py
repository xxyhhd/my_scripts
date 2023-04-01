from tools import ToolsCmd
from rich.console import Console


console = Console()

def chang_user(port):
    console.print('\n5-开始修改工作目录权限', style="bold yellow")
    ToolsCmd('chown -R mysql.mysql /dbs/mysqls/mysql{0}'.format(port))
    ToolsCmd('chmod -R 755 /dbs/mysqls/mysql{0}'.format(port))
    console.print('修改工作目录权限成功', style="bold green")
    return True