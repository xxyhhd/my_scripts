from time import time
import os
from tools.tool_cmd import ssh_cli


class create_html():
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host, dbname, port, user, passwd, file_path, comment='Mysql'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.filename = os.path.join(file_path, comment + '_' + host + '_' + str(port) + '_' + str(round(time()))) + '.html'
        self.css = '''
<html>
<head>
<style type="text/css">
    body        {font:20px Courier New,Helvetica,sansserif; color:black; background:White;}
    table,tr,td {font:20px Courier New,Helvetica,sansserif; color:Black; background:rgb(236, 191, 143); padding:0px 0px 0px 0px; margin:0px 0px 0px 0px;} 
    th          {font:bold 20px Courier New,Helvetica,sansserif; color:White; background:#0033FF; padding:0px 0px 0px 0px;} 
    h1          {font:bold 20pt Courier New,Helvetica,sansserif; color:Black; padding:0px 0px 0px 0px;} 
</style>
</head>
<body>
        '''


    # 在html文件写入css样式
    def create_css_on_html(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('{}\n'.format(self.css)) 


    # 写HTML标题的函数
    def create_head_on_html(self, text):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('<h1>{}</h1>\n'.format(text))


    # 创建表格的函数1
    def create_table_head1(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('<table width="68%" border="1" bordercolor="#000000" cellspacing="0px" style="border-collapse:collapse">\n')


    # 创建表格的函数1
    def create_table_head2(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('<table width="100%" border="1" bordercolor="#000000" cellspacing="0px" style="border-collapse:collapse">\n')

    # 创建tr前区间函数
    def create_tr_begin(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('<tr>\n')
    

    # 创建tr后区间函数
    def create_tr_end(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('</tr>\n')


    # 创建表头函数
    def create_th(self, ths):
        with open(self.filename, 'a', encoding='utf-8') as f:
            self.create_tr_begin()
            for th in ths:
                f.writelines('<th>{}</th>\n'.format(th))
            self.create_tr_end()


    # 写表格数据函数
    def create_td(self, td, colar='green'):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('<td style="color:{1}">{0}</td>\n'.format(td, colar))


    # 创建表格结尾函数
    def create_table_end(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('{}\n'.format('</table>'))  


    # 创建html文件结尾函数
    def create_html_end(self):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.writelines('{}\n'.format('</body></html>'))        


class get_os_info(create_html):
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_os_version(self):
        try:
            hostname = ssh_cli(self.host, 'uname -n')[0]
            uptime_return = ssh_cli(self.host, 'uptime')[0].split()


# print(aa.split(': ')[1])
# print(aa.split(': ')[0].split('up ')[1].split(',')[0])

        except:
            return False
            print('出错了!!!!!!!')

        self.create_css_on_html()
        self.create_head_on_html('基本信息')
        self.create_table_head1()
        # self.create_th(('name', 'age', 'sex'))
        self.create_tr_begin()

        self.create_td('主机名')
        self.create_td(hostname)

        self.create_td('运行时间')
        self.create_td(uptime, 'red')

        self.create_tr_end()



        self.create_table_end()
        self.create_html_end()




    


if __name__ == '__main__':
    mysql_mo = get_os_info(host='192.168.122.102', dbname='test', port=3306, user='root', passwd='123456', file_path='/root/my_scripts', comment = '测试实例')
    mysql_mo.get_os_version()