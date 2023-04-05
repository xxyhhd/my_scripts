import getpass
import os
import re
import datetime


def con_db(host, port, user, passwd, db_name, tb_name):
    try:
        import pymysql
        from warnings import filterwarnings
        filterwarnings("error",category=pymysql.Warning)
    except:
        print('在线模式依赖pymysql，请先安装：pip3 install pymysql')
        return False

    try:
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db_name)
        cursor = conn.cursor()
        cursor.execute("select column_name from information_schema.columns WHERE table_schema = '{0}' and table_name = '{1}' ORDER BY ORDINAL_POSITION;".format(db_name, tb_name))
        res = cursor.fetchall()
        conn.close()
        columns = []
        for column in res:
            columns.append(column[0])
        return (columns)
    except pymysql.Error as e:
        print (repr(e))
    

def format_insert_sql(file_path, db_tb):
    os.system('echo "--" >> {}'.format(file_path))
    sql_time= ''
    sql_set = []
    insert_n, switch = 0, 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if re.match('#', line) and 'server id' in line and 'end_log_pos' in line:
                sql_time = line.split('server id')[0]
                continue

            if 'INSERT INTO {0}'.format(db_tb) == line.strip():
                switch = 0
                insert_n += 1
                if insert_n > 1:
                    print('INSERT INTO {0}'.format(db_tb) + ' SET ' + ', '.join(sql_set[1:]) + ';  ' + sql_time + '原始sql')
                    print('DELETE FROM {0}'.format(db_tb) + ' WHERE ' + ' AND '.join(sql_set[1:]) + ';  ' + sql_time + '反转sql')
                    sql_set = []

            if 'SET' == line.strip():
                switch = 2

            if '--' == line.strip():
                print('INSERT INTO {0}'.format(db_tb) + ' SET ' + ', '.join(sql_set[1:]) + ';  ' + sql_time + '原始sql')
                print('DELETE FROM {0}'.format(db_tb) + ' WHERE ' + ' AND '.join(sql_set[1:]) + ';  ' + sql_time + '反转sql')
                sql_set, switch, insert_n = [], 0, 0

            if 'INSERT INTO {0}'.format(db_tb) != line.strip() or 'SET' != line.strip() or '--' != line.strip() or not (re.match('#', line) and 'server id' in line and 'end_log_pos' in line):
                if switch == 2:
                    sql_set.append(line.strip())


def format_delete_sql(file_path, db_tb):
    os.system('echo "--" >> {}'.format(file_path))
    sql_time= ''
    sql_where = []
    delete_n, switch = 0, 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if re.match('#', line) and 'server id' in line and 'end_log_pos' in line:
                sql_time = line.split('server id')[0]
                continue

            if 'DELETE FROM {0}'.format(db_tb) == line.strip():
                switch = 0
                delete_n += 1
                if delete_n > 1:
                    print('DELETE FROM {0}'.format(db_tb) + ' WHERE ' + ' AND '.join(sql_where[1:]) + ';  ' + sql_time + '原始sql')
                    print('INSERT INTO {0}'.format(db_tb) + ' SET ' + ', '.join(sql_where[1:]) + ';  ' + sql_time + '反转sql')
                    sql_where = []

            if 'WHERE' == line.strip():
                switch = 1

            if '--' == line.strip():
                print('DELETE FROM {0}'.format(db_tb) + ' WHERE ' + ' AND '.join(sql_where[1:]) + ';  ' + sql_time + '原始sql')
                print('INSERT INTO {0}'.format(db_tb) + ' SET ' + ', '.join(sql_where[1:]) + ';  ' + sql_time + '反转sql')
                sql_where, switch, delete_n = [], 0, 0

            if 'DELETE FROM {0}'.format(db_tb) != line.strip() or 'WHERE' != line.strip() or '--' != line.strip() or not (re.match('#', line) and 'server id' in line and 'end_log_pos' in line):
                if switch == 1:
                    sql_where.append(line.strip())


def format_update_sql(file_path, db_tb):
    os.system('echo "--" >> {}'.format(file_path))
    sql_time= ''
    sql_where, sql_set = [], []
    update_n, switch = 0, 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if re.match('#', line) and 'server id' in line and 'end_log_pos' in line:
                sql_time = line.split('server id')[0]
                continue

            if 'UPDATE {0}'.format(db_tb) == line.strip():
                switch = 0
                update_n += 1
                if update_n > 1:
                    print('UPDATE {0}'.format(db_tb) + ' SET ' + ', '.join(sql_set[1:]) + ' WHERE ' + ' AND '.join(sql_where[1:]) + ';  ' + sql_time + '原始sql')
                    print('UPDATE {0}'.format(db_tb) + ' SET ' + ', '.join(sql_where[1:]) + ' WHERE ' + ' AND '.join(sql_set[1:]) + ';  ' + sql_time + '反转sql')
                    sql_where, sql_set = [], []

            if 'WHERE' == line.strip():
                switch = 1

            if 'SET' == line.strip():
                switch = 2

            if '--' == line.strip():
                print('UPDATE {0}'.format(db_tb) + ' SET ' + ', '.join(sql_set[1:]) + ' WHERE ' + ' AND '.join(sql_where[1:]) + ';  ' + sql_time + '原始sql')
                print('UPDATE {0}'.format(db_tb) + ' SET ' + ', '.join(sql_where[1:]) + ' WHERE ' + ' AND '.join(sql_set[1:]) + ';  ' + sql_time + '反转sql')
                sql_where, sql_set, switch, update_n = [], [], 0, 0

            if 'UPDATE {0}'.format(db_tb) != line.strip() or 'WHERE' != line.strip() or 'SET' != line.strip() or '--' != line.strip() or not (re.match('#', line) and 'server id' in line and 'end_log_pos' in line):
                if switch == 1:
                    sql_where.append(line.strip())

                if switch == 2:
                    sql_set.append(line.strip())

  
def get_command():
    while True:
        print('************** 1. 请选择在线模式或离线模式 **************\n1：离线模式（该模式需要提供表结构等信息）\n2：在线模式（该模式需要提供数据库账号密码）\nq：退出')
        flash_mode = input('请输入你的选择：')
        if flash_mode not in ('1', '2', 'q'):
            print('参数选择不合法')
            continue
        if flash_mode == 'q':
            break
        
        print('\n************** 2. 请提供需要闪回的表信息 **************\n')
        db_name = input('请输入库名（大小写敏感）：') or 'testdb'
        tb_name = input('请输入表名（大小写敏感）：') or 'testtb'
        if flash_mode == '1':
            table_info = input('请输入表的列信息（列之间用","分隔，且顺序不可颠倒）：') or 'id,name,email'
            table_column = table_info.split(',')
        else:
            db_host = input('请输入数据库连接地址：') or '127.0.0.1'
            db_port = int(input('请输入数据库连接端口：'))
            db_user = input('请输入数据库连接用户：') or 'root'
            db_passwd = getpass.getpass('请输入数据库连接密码：') or '123456'
            table_column = con_db(db_host, db_port, db_user, db_passwd, db_name, tb_name)
            if not table_column:
                break   

        print('\n************** 3. 请提供Binlog文件及反转SQL保存目录 **************\n')
        mysqlbinlog_path = input('请提供mysqlbinglog工具的绝对路径：') or '/usr/local/mysql/bin/mysqlbinlog'
        binlog_path = input('请提供Binlog文件所在绝对路径：') or '/usr/local/mysql/data/binlog.000003'
        base_path = input('请提供反转SQL保存目录，默认存放/tmp：') or '/tmp'
        save_path = base_path.rstrip('/')+'/'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'/'
        os.system('mkdir {}'.format(save_path))

        print('\n************** 4. 请选择客户错误执行的SQL类型 **************\n1：INSERT\n2：DELETE\n3：UPDATE')
        error_action = input('请输入你的选择：') or '3'
        if error_action not in ('1', '2', '3'):
            print('参数选择不合法')
            continue
        if error_action == '1':
            action = 'INSERT'
            N = len(table_column) + 1
        if error_action == '2':
            action = 'DELETE'
            N = len(table_column) + 1
        if error_action == '3':
            action = 'UPDATE'
            N = len(table_column) * 2 + 2

        print('\n************** 5. 请选择反转方式和反转内容 **************\n1：根据时间范围反转\n2：根据position反转\n3：反转全部\n')
        flash_method = input('请输入你的选择（默认反转全部）：') or '3'
        if flash_method not in ('1', '2', '3'):
            print('参数选择不合法')
            continue
        if flash_method == '1':  # 根据时间选择
            start_time = input('请输入起始时间（示例：2023-03-14 10:45:00）：')
            stop_time = input('请输入结束时间（示例：2023-03-14 11:45:00）：')
            os.system("{0} --base64-output=decode-rows -vvv --start-datetime='{7}' --stop-datetime='{8}' {1} |egrep -B 1  -A {2} '{3}( INTO | | FROM )`{4}`.`{5}`' |sed 's/\/.*\///g' > {6}sql.tmp".format(mysqlbinlog_path, binlog_path, N, action, db_name, tb_name, save_path, start_time, stop_time))
        elif flash_method == '2':  # 根据position选择
            start_postion = input('请输入起始position（示例：4）：')
            stop_position = input('请输入结束position（示例：954）：')
            os.system("{0} --base64-output=decode-rows -vvv --start-position={7} --stop-position={8} {1} |egrep -B 1  -A {2} '{3}( INTO | | FROM )`{4}`.`{5}`' |sed 's/\/.*\///g' > {6}sql.tmp".format(mysqlbinlog_path, binlog_path, N, action, db_name, tb_name, save_path, start_postion, stop_position))
        else:
            os.system("{0} --base64-output=decode-rows -vvv {1} |egrep -B 1  -A {2} '{3}( INTO | | FROM )`{4}`.`{5}`' |sed 's/\/.*\///g' > {6}sql.tmp".format(mysqlbinlog_path, binlog_path, N, action, db_name, tb_name, save_path))
        for x in range(len(table_column)):
            os.system("sed -i '' 's/###   @{0}=/{1}=/g' {2}sql.tmp".format(x+1, table_column[x], save_path))
        os.system("sed -i '' 's/### //g' {0}sql.tmp".format(save_path))
        return(action, save_path, db_name, tb_name)


def main():
    command = get_command()
    if command[0] == 'INSERT':
        format_insert_sql('{}sql.tmp'.format(command[1]), '`{0}`.`{1}`'.format(command[2], command[3]))
    if command[0] == 'UPDATE':
        format_update_sql('{}sql.tmp'.format(command[1]), '`{0}`.`{1}`'.format(command[2], command[3]))
    if command[0] == 'DELETE':
        format_delete_sql('{}sql.tmp'.format(command[1]), '`{0}`.`{1}`'.format(command[2], command[3]))
    print('结果集存放目录：' + command[1])


main()
