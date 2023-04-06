from tools.condb import db
from rich.console import Console
# from rich.table import Table


console = Console()
# table = Table()
# table.add_column('[blue]insname')
# table.add_column('[blue]db_type')
# table.add_column('[blue]vip_host')
# table.add_column('[blue]vip_port')
dbaas = db('192.168.122.102', 'dbaas', 3306)
