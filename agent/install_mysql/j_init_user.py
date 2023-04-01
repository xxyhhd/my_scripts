from tools import ToolsCmd
from rich.console import Console


console = Console()

def init_user(port, db_v):
    console.print('\n9-初始化账号权限', style="bold yellow", highlight=True)
    if '5.6' in db_v:
        ToolsCmd("/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /root/agent/setuser56.sql".format(port))
    else:
        ToolsCmd("/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock < /root/agent/setuser.sql".format(port))
    console.print('账号初始化成功', style="bold green", highlight=True)