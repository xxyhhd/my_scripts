from generic_scripts.tools import ssh_cli, ToolsCmd
import re
import time


r1 = ToolsCmd('virsh start centos7')[0]
if re.search('已开始', r1):
    time.sleep(30)
    print(ssh_cli('centos7', 'docker exec -it ab25dbb9bacc bash -c "/root/anaconda3/bin/python /date/aaa.py &"'))