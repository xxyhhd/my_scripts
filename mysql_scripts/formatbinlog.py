import os
import re

a = '/tmp/aaa.tmp'



def format_all_sql(file_path):
    save_insert, save_update, save_delete = False, False, False
    sql_position, sql_time, exec_time = '', '', ''
    print_res = ''
    with open(file_path, 'r', encoding='utf-8') as f1:
        for line in f1:
            if re.match('^SET TIMESTAMP=', line) or re.match('^/\*!', line) or re.match('^SET @@session', line, re.IGNORECASE):
                continue
            if re.match('^# at [0-9]*', line):
                sql_position = re.findall('\d*', line)[5]
                save_insert, save_update, save_delete = False, False, False
                if print_res != '':
                    print(print_res, format_note)
                print_res = ''
            if re.match('^#.*server id.*end_log_pos.*', line):
                sql_time = re.findall('\d{6} \d{2}:\d{2}:\d{2}', line)[0]
                if re.match('^#.*server id.*end_log_pos.*Query.*', line):
                    exec_time = re.findall('exec_time=\d*', line)[0].split('=')[1]
                    format_note = "#position： {0}，  start_time：{1},  exec_time：{2}".format(sql_position, sql_time, exec_time)
                    print('# BEGIN    ' + format_note)
                format_note = "#position： {0}，  start_time：{1},  exec_time：{2}".format(sql_position, sql_time, exec_time)
            if re.match('^use `.*`', line, re.IGNORECASE):
                print(re.findall('^use `.*`', line)[0] + ';   ' + format_note)
            if re.match('^create |^alter |^drop |^truncate', line, re.IGNORECASE):
                print(re.findall('^create .*|^alter .*|^drop .*|^truncate .*', line, re.IGNORECASE)[0] + ';  ' + format_note)
            if save_insert:
                if re.match('^### INSERT INTO ', line) and print_res != '':
                    print(print_res, format_note)
                    print_res = ''
                print_res += re.sub('/\*.*\*/','',re.sub('^### ','',line.strip())) +' '
            if save_update:
                if re.match('^### UPDATE ', line) and print_res != '':
                    print(print_res, format_note)
                    print_res = ''
                print_res += re.sub('/\*.*\*/','',re.sub('^### ','',line.strip())) +' '
            if save_delete:
                if re.match('^### DELETE FROM ', line) and print_res != '':
                    print(print_res, format_note)
                    print_res = ''
                print_res += re.sub('/\*.*\*/','',re.sub('^### ','',line.strip())) +' '


            if re.match('^#.*server id.*end_log_pos.*Write_rows.*', line):
                save_insert = True
            if re.match('^#.*server id.*end_log_pos.*Update_rows.*', line):
                save_update = True
            if re.match('^#.*server id.*end_log_pos.*Delete_rows.*', line):
                save_delete = True



format_all_sql(a)