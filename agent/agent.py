import sys
from db_tools import *
import os


action = sys.argv[1]
port = sys.argv[2]
db_v = sys.argv[3]


def main():
    if action == 'install':
        return (install_mysql(port, db_v))
    # elif action == '10':
    #     remove_db(port, db_v)
    # elif action == '4':
    #     start_mysql(port)
    # elif action == '5':
    #     stop_mysql(port)
    return True

main()

