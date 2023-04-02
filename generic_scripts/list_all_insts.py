from generic_scripts.gen_class import dbaas, console, table



def list_insts():
    console.print('************** 实例列表如下 **************', style="bold green")
    inst_names = dbaas.ReadFromMysql('select ins_name, db_v, ip, port from ins_info where used = 1 and role = 0;')
    table.add_column('[blue]insname')
    table.add_column('[blue]db_type')
    table.add_column('[blue]vip_host')
    table.add_column('[blue]vip_port')
    for inst_name in inst_names:
        table.add_row('[green]{}'.format(inst_name[0]), '[green]{}'.format(inst_name[1]), '[green]{}'.format(inst_name[2]), '[green]{}'.format(inst_name[3]))
    console.print(table)
    print('\n\n')

