from generic_scripts.tools import ToolsCmd, ssh_cli
from generic_scripts.global_var import logger, console, dbaas
from db_scripts.mysql import login_mysql, install_mysql, start_mysql, stop_mysql, remove_mysql
from db_scripts.redis import login_redis, start_redis, stop_redis, install_redis, remove_redis
from db_scripts.pgsql import login_pgsql, start_pgsql, stop_pgsql, install_pgsql, remove_pgsql
import time
import random
import inspect
import os


def list_dbs():
    from rich.table import Table
    table = Table()
    table.add_column('[blue]insname')
    table.add_column('[blue]db_type')
    table.add_column('[blue]vip_host')
    table.add_column('[blue]vip_port')
    list_insts_sql = 'select ins_name, db_v, ip, port, vip_port from ins_info where used = 1 and role = 0;'
    console.print('************** 实例列表如下 **************', style="bold green")
    dbaas.execute(list_insts_sql)
    inst_names = dbaas.fetchall()
    for inst_name in inst_names:
        if inst_name[4] is None:
            table.add_row('[green]{}'.format(inst_name[0]), '[green]{}'.format(inst_name[1]), '[green]{}'.format(inst_name[2]), '[green]{}'.format(inst_name[3]))
        else:
            table.add_row('[green]{}'.format(inst_name[0]), '[green]{}'.format(inst_name[1]), '[green]{}'.format('192.168.124.100'), '[green]{}'.format(inst_name[4]))
    console.print(table)


def info_db():
    from rich.table import Table
    table1 = Table()
    table1.add_column('[blue]insname')
    table1.add_column('[blue]db_type')
    table1.add_column('[blue]role')
    table1.add_column('[blue]host')

    console.print('\n************** 开始查询实例信息 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))    
    info_db_sql = 'select ins_name, db_v, role, concat(ip, ":", port) from ins_info where ins_name = "{}" order by role'.format(inst_name)
    dbaas.execute(info_db_sql)
    info_inst = dbaas.fetchall()
    for info in info_inst:
        table1.add_row('[green]{}'.format(info[0]), '[green]{}'.format(info[1]), '[green]{}'.format(info[2]), '[green]{}'.format(info[3]))
    console.print(table1)


def login_db():
    console.print('\n************** 输入实例名 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名（默认登录dbaas）：')) or 'dbaas'
    inst_info_sql = 'select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name)
    dbaas.execute(inst_info_sql)
    inst_info = dbaas.fetchall()
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        login_mysql(inst_info)
    elif 'redis' in inst_info[0][2]:
        login_redis(inst_info)
    elif 'postgres' in inst_info[0][2]:
        login_pgsql(inst_info)


def install_db():
    def ass_resource(ins_num, db_type):
        get_ips_sql = 'SELECT id, ip, port from ins_info where used = 0 and db_type = "{0}" group by ip order by count(ip) desc limit {1} for update;'.format(db_type, ins_num)
        dbaas.execute(get_ips_sql)
        inst_info = dbaas.fetchall()
        if len(inst_info) != ins_num:
            console.print('主机资源不足，无法创建实例', style="bold red")
            return False
        else:
            for inst in inst_info:
                dbaas.execute('update ins_info set used = 1 where id={};'.format(inst[0])) 
        dbaas.commit()
        return inst_info


    norms = {1: 'MySQL', 2: 'Redis', 3: 'PgSql'}
    console.print('\n************** 请选择数据库类型 **************', style="bold yellow")
    for k, v in norms.items():
        console.print('{0}: {1}'.format(k,v), style="bold white")
    db_type = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认MySQL）')) or '1'

    # 获取实例规格
    norms_norm = {1: '单节点', 2: '双节点', 3: '三节点'}
    console.print('\n************** 请选择实例规格 **************', style="bold yellow")
    for k, v in norms_norm.items():
        console.print('{0}: {1}'.format(k,v), style="bold white")
    inst_num = input("\033[5;34m{0}\033[0m".format('请输入你的选择（默认双节点）：')) or '2'   # 实例规格
    inst_num = int(inst_num)

    if db_type == '1':
        install_mysql(ass_resource(inst_num, 'mysql'))
    elif db_type == '2':
        install_redis(ass_resource(inst_num, 'redis'))
    elif db_type == '3':
        install_pgsql(ass_resource(inst_num, 'postgresql'))
    else:
        console.print('很抱歉，参数不合法！！！', style="bold red")


def remove_db():
    console.print('\n************** 开始删除实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入待删除的实例名：'))
    dbaas.execute('select ip, port, db_type from ins_info where ins_name = "{}"'.format(inst_name))
    inst_info = dbaas.fetchall()
    if len(inst_info) > 0:
        for inst in inst_info:
            if inst[2] == 'mysql':
                remove_mysql(inst[0], inst[1])
            if inst[2] == 'redis':
                remove_redis(inst[0], inst[1])
            elif inst[2] == 'postgresql':
                remove_pgsql(inst[0], inst[1])
        dbaas.execute("update ins_info ii, vip_port vp set ii.vip_port=NULL, vp.used=0 where ii.ins_name = '{}' and ii.vip_port = vp.port;".format(inst_name))
        dbaas.execute("update ins_info set used=0, ins_name=NULL, role=NULL, db_v=NULL where ins_name = '{}';".format(inst_name))
        dbaas.commit()
        console.print('实例已删除', style="bold green")
        ToolsCmd('rm -fr /etc/nginx/conf.d/{}.conf'.format(inst_name))
        ToolsCmd('/usr/local/nginx/sbin/nginx -c /etc/nginx/nginx.conf -s reload')
        console.print('实例已从Nginx移除', style="bold green")
    else:
        console.print('该实例不存在！！！！', style="bold red")  


def stop_db():
    console.print('\n************** 开始停止实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))
    dbaas.execute('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    inst_info = dbaas.fetchall()
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        for inst in inst_info:
            stop_mysql(inst[0], inst[1])
    elif 'redis' in inst_info[0][2]:
        for inst in inst_info:
            stop_redis(inst[0], inst[1])
    elif 'postgres' in inst_info[0][2]:
        for inst in inst_info:
            stop_pgsql(inst[0], inst[1])


def start_db():
    console.print('\n************** 开始启动实例 **************', style="bold yellow")
    inst_name = input("\033[5;34m{0}\033[0m".format('请输入实例名：'))
    dbaas.execute('select ip, port, db_v from ins_info where ins_name = "{}" order by role'.format(inst_name))
    inst_info = dbaas.fetchall()
    if len(inst_info) == 0:
        console.print('实例不存在\n\n', style="bold red")
        return False
    if 'mysql' in inst_info[0][2]:
        for inst in inst_info:
            start_mysql(inst[0], inst[1])
    elif 'redis' in inst_info[0][2]:
        for inst in inst_info:
            start_redis(inst[0], inst[1])
    elif 'postgres' in inst_info[0][2]:
        for inst in inst_info:
            start_pgsql(inst[0], inst[1])


