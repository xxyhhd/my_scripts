from generic_scripts.gen_class import console, dbaas


def ass_resource(ins_num, db_type):
    where = ''
    res = {}
    for ins in range(ins_num):
        inst_info = dbaas.RWMsql(('select id into @id from ins_info where used = 0 and db_type = "{0}" {1} group by ip order by count(ip) desc limit 1 for update;'.format(db_type, where), 'update ins_info set used = 1 where id=@id;', 'select id, ip, port from ins_info where id = @id;'))
        if len(inst_info[1]) == 0:
            console.print('主机资源不足，无法创建实例', style="bold yellow")
            for x in res:
                dbaas.WriteToMysql('update ins_info set used = 0 where id={}'.format(res[x][0]))
            return False
        else:
            res[ins] = inst_info[1][0]
        where = where + 'and ip !="{0}" '.format(inst_info[1][0][1])
    return res



 