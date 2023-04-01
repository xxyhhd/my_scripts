import os
from rich.console import Console


console = Console()


def rm_dir(port):
    path = '/dbs/mysqls/mysql{0}'.format(port)
    while True:
        if input("\033[5;34m{0}\033[0m".format('\n你的选择：')) == 'yes':
            break
    os.system('rm -fr /dbs/mysqls/mysql{0}'.format(port))
    console.print('目录已删除，任务将继续', style="bold yellow")
    return True