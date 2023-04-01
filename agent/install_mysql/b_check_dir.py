import os
from rich.console import Console


console = Console()


def check_dir(port):
    path = '/dbs/mysqls/mysql{0}'.format(port)
    console.print('2-检查目录是否存在：{0}\n'.format(path), style="bold yellow")
    if  os.path.exists(path):
        console.print('目录非空，请检查数据是否有用并确认是否可以删除\n可以删除请输入yes\n不能删除请”Ctrl + C“取消安装并执行删除脏实例任务'.format(path), style="bold red", highlight=True)
        return False
    console.print('目录存在性检查通过：{0}\n'.format(path), style="bold green")
    return True