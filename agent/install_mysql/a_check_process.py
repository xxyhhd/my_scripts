import os
from rich.console import Console
from tools import ToolsCmd

console = Console()


def check_proc(port):
    console.print('\n1-检查端口是否被占用', style="bold yellow")
    while True:
        res = ToolsCmd('ps -ef |grep {} |grep -v "python3" |grep -v "grep"'.format(port))
        if res[0] != '':
            suggest = ToolsCmd("ps -ef |grep my%s |grep -v 'grep' |grep -v 'python' |awk '{print $2}'"%(port))
            console.print(res[0], style="bold blue")
            console.print('端口可能已经被进程占用，请人工检查\n可以kill的进程请输入"kill -9 id1; kill -9 id2"\n不能kill请”Ctrl + C“取消安装并执行删除脏实例任务', style="bold red", highlight=True)
            sugg = suggest[0].strip().split('\n')
            a = ''
            for x in sugg:
                a = a + 'kill -9 ' + x + ';'
            console.print('kill建议: {0}'.format(a), style="bold yellow")
            kill_command =  input("\033[5;34m{0}\033[0m".format('\n你的选择：'))
            os.system(kill_command)
            continue
        break
    console.print('端口占用检查通过\n', style="bold green")
