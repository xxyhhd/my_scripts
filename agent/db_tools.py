# import os
# import time
# from datetime import datetime
# from tools import ToolsCmd, get_db_package
from install_mysql.a_check_process import check_proc
from install_mysql.b_check_dir import check_dir
from install_mysql.c_mkdir import mkdir
from install_mysql.d_rmdir import rm_dir
from install_mysql.e_ln_to_pachage import ln
from install_mysql.f_change_file_owner import chang_user
from install_mysql.g_build_cnf import cnf
from install_mysql.h_init_mysql import init_mysql
from install_mysql.i_start_mysql import start_mysql
from install_mysql.j_init_user import init_user


def install_mysql(port, db_v):
    check_proc(port)
    if check_dir(port) is False:
        rm_dir(port)
    mkdir(port)
    ln(port, db_v)
    chang_user(port)
    cnf(port)
    init_mysql(port, db_v)
    start_mysql(port)
    init_user(port, db_v)


