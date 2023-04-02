from tools import ToolsCmd
from rich.console import Console


console = Console()

def build_slave(master_host, master_port, slave_port, username, passwd):
    console.print('\n10-搭建主从复制', style="bold yellow", highlight=True)
    sql = "change master to master_host='{0}',master_port={1},master_user='{2}',master_password='{3}',master_auto_position=1; ".format(master_host, master_port, username, passwd)
    ToolsCmd("/dbs/mysqls/mysql{0}/service/bin/mysql -S /tmp/mysql{0}.sock -p123456 -e \"{1}\" ".format(slave_port, sql))
    console.print('账号初始化成功', style="bold green", highlight=True)

build_slave('192.168.122.102', 3306, 3307, 'backup', 'backup')