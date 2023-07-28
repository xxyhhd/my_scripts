from generic_scripts.class_log import DualLogger
from generic_scripts.class_db import Mysql_Db
from rich.console import Console


console = Console()
logger = DualLogger('/tmp/log.txt')
dbaas = Mysql_Db('dbaas', 'root', '123456', '127.0.0.1', 3306)
