from tools.condb import db
from rich.console import Console
from rich.table import Table


console = Console()
table = Table()
dbaas = db('192.168.122.102', 'dbaas', 3306)