from generic_scripts.tools import ToolsCmd, ssh_cli
from generic_scripts.global_var import logger, console, dbaas


def set_nginx(ins_name):
    dbaas.execute('select ip, port from ins_info where ins_name = "{}" order by role limit 2;'.format(ins_name))
    inst_info = dbaas.fetchall()
    if len(inst_info) == 2:
        # 获取并占用vip_port
        dbaas.execute('select port from vip_port where used = 0 limit 1 for update;')
        vip_port = dbaas.fetchone()[0]
        dbaas.execute('update vip_port set used = "1" where port = {}'.format(vip_port))
        dbaas.execute('update ins_info set vip_port = {} where ins_name = "{}"'.format(vip_port, ins_name))
        dbaas.commit()
        nginx_file = '/etc/nginx/conf.d/{}.conf'.format(ins_name)
        ToolsCmd('cp /root/my_scripts/new/nginx.conf {}'.format(nginx_file))
        ToolsCmd("sed -i 's/real_server_a/{0}:{1}/g' {2}".format(inst_info[0][0], inst_info[0][1], nginx_file))
        ToolsCmd("sed -i 's/real_server_b/{0}:{1}/g' {2}".format(inst_info[1][0], inst_info[1][1], nginx_file))
        ToolsCmd("sed -i 's/inst_name/{0}/g' {1}".format(ins_name, nginx_file))
        ToolsCmd("sed -i 's/port/{0}/g' {1}".format(vip_port, nginx_file))
        ToolsCmd('/usr/local/nginx/sbin/nginx -c /etc/nginx/nginx.conf -s reload')


    

