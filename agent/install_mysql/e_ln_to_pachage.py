import os
from rich.console import Console
from tools import ToolsCmd
from tools import get_db_package

console = Console()
def ln(port, db_v):
    console.print('\n4-开始查找适合的版本并创建软链接', style="bold yellow")
    package = get_db_package(db_v)
    ToolsCmd('ln -s {0} /dbs/mysqls/mysql{1}/service'.format(package, port))
    console.print('软链接创建成功', style="bold green")

