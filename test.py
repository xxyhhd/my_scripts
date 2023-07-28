import subprocess
from new.generic_scripts.tools import ssh_cli

psql = '/dbs/versions/postgresql-15.2/bin/psql '
user = 'pgsql4007'
port = '4007'
dbname = 'postgres'
host = '192.168.122.101'


temp_cnf = '''
listen_addresses = '0.0.0.0'  # 备库的监听地址，可以接受来自任何地址的连接
port = {0}  # 监听端口

shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all

max_connections = 100  # 最大连接数
superuser_reserved_connections = 10  # 保留给超级用户的连接数

wal_level = replica  # WAL 日志级别
archive_mode = on  # 开启归档模式
archive_command = 'cp %p /dbs/pgsql/pgsql{0}/archive/%f'  # 归档命令，将 WAL 日志复制到归档目录

hot_standby = on  # 开启热备
max_wal_senders = 10  # 最大 WAL 发送者数
wal_keep_segments = 32  # 保留的 WAL 日志段数
hot_standby_feedback = on  # 启用热备反馈

shared_buffers = 4GB  # 共享缓冲区大小
effective_cache_size = 12GB  # 有效缓存大小
work_mem = 64MB  # 每个连接的工作内存
maintenance_work_mem = 1GB  # 维护操作的内存
'''.format(port)


ssh_cli('192.168.122.101', "echo {} > /root/bbb.postgres.cnf".format(temp_cnf))


# print(temp_cnf)

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error is not None:
        raise Exception("Command '%s' failed with error: %s" % (command, error))
    return output.strip().decode('utf-8')


# print(execute_command("ssh {} -t 'ps -ef |grep postgres'".format(host)))

# sql = "select datname from pg_database where datistemplate=false and datname !='postgres'"
# dbnames = str(execute_command('{0} -U {1} -h {2} -p {3} -d {4} -c "{5}"'.format(psql, user, host, port, dbname, sql)))
# for dbname in dbnames.split('\n')[2:-1]:
#     sql = "select concat(schemaname, '.', tablename) from pg_tables where tableowner != 'pgsql4007';"
#     tables = str(execute_command('{0} -U {1} -h {2} -p {3} -d {4} -c "{5}"'.format(psql, user, host, port, dbname, sql)).decode('utf-8'))
#     print(tables.split('\n')[2:-1])


