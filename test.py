from tools.tool_cmd import ssh_cli


print(ssh_cli('192.168.122.101', 'whoami', username='pgsql6000', password='password'))
print(ssh_cli('192.168.122.101', 'whoami'))

