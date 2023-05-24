from tools.condb import db
from rich.console import Console
# from rich.table import Table


console = Console()

dbaas = db('127.0.0.1', 'dbaas', 3306)
