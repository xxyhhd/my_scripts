class command():
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        self.port = kwargs.get('port')



        # 查看进程信息，返回进程信息
        self.pgsql_ops_command_check_process_info = "ps -ef |grep 'dbs/pgsql/pgsql{}/data' |grep -v grep".format(self.port)
        self.redis_ops_command_check_process_info = "ps -ef |grep redis-server |grep :{} |grep -v grep".format(self.port)
        self.mysql_ops_command_check_process_info = "ps -ef |grep mysqld |grep my{} |grep -v grep".format(self.port)

        # 查看进程信息，返回进程号
        self.pgsql_ops_command_check_process_info = "ps -ef |grep 'dbs/pgsql/pgsql{}/data' |grep -v grep".format(self.port)
        self.redis_ops_command_check_process_info = "ps -ef |grep redis-server |grep :{} |grep -v grep".format(self.port)
        self.mysql_ops_command_check_process_info = "ps -ef |grep mysqld |grep my{} |grep -v grep".format(self.port)

        # 查看进程信息，返回进程数
        self.pgsql_ops_command_check_process_info = "ps -ef |grep 'dbs/pgsql/pgsql{}/data' |grep -v grep".format(self.port)
        self.redis_ops_command_check_process_info = "ps -ef |grep redis-server |grep :{} |grep -v grep".format(self.port)
        self.mysql_ops_command_check_process_info = "ps -ef |grep mysqld |grep my{} |grep -v grep".format(self.port)



        # 修改pg_hba.conf文件
        self.pgsql_ops_command_white_ip = "echo 'host all all 0.0.0.0/0 trust' > /dbs/pgsql/pgsql{}/data/pg_hba.conf".format(self.port)
        # 置空postgresql.conf 文件
        self.pgsql_ops_command_white_ip = "echo 'host all all 0.0.0.0/0 trust' > /dbs/pgsql/pgsql{}/data/pg_hba.conf".format(self.port)



if __name__ == '__main__':
    test = command(port=3306)
    print(test.pgsql_ops_command_check_process_info)
