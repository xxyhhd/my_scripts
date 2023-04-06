from tools.tool_cmd import ssh_cli
from generic_scripts.gen_class import console
import datetime


def full_backup_mysql(inst_info):
    norms = {1: 'master', 2: 'slave', 3: 'logger'}
    console.print('************** 请输入实例角色，提示：该实例只有{}个节点 **************'.format(len(inst_info)), style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold yellow")
    inst_role = input("\033[5;34m{0}\033[0m".format('请输入备份角色：')) or '1'
    inst_role = int(inst_role) - 1
    if inst_role > len(inst_info) - 1:
        console.print('抱歉，该实例不存在所选角色', style="bold red")
        return False
    host, port, db_v = inst_info[inst_role]
    backup_path = '/dbs/mysqls/backup/{0}/{1}/'.format(port, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    ssh_cli(host, 'mkdir -p {}'.format(backup_path))
    if db_v == 'mysql-8':
        package_path = ssh_cli(host, 'find /dbs/versions -maxdepth 1 -name {}* |tail -1'.format('percona-xtrabackup-8'))[0].strip()
        cmd_backup = '{0}/bin/xtrabackup --defaults-file=/etc/my{1}.cnf --host=127.0.0.1 --port={1} --user=root --password=123456 --backup --target-dir={2} 2>{2}backup.log &'.format(package_path, port, backup_path)
    else:
        package_path = ssh_cli(host, 'find /dbs/versions -maxdepth 1 -name {}* |tail -1'.format('percona-xtrabackup-2'))[0].strip()
        cmd_backup = '{0}/bin/innobackupex --defaults-file=/etc/my{1}.cnf --host=127.0.0.1 --port={1} --user=root --password=123456 --no-timestamp {2} 2>{2}backup.log &'.format(package_path, port, backup_path)
    ssh_cli(host, cmd_backup)
    console.print('备份路径主机：{0}，备份路径：{1}'.format(host, backup_path), style="bold green")
