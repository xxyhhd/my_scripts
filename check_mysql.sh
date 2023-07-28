#!/bin/bash


MYSQL_SERVERS=("192.168.122.102:3306" "192.168.122.103:3306")
USER="root"
PASS="123456"

for SERVER in "${MYSQL_SERVERS[@]}"; do
    HOST=${SERVER%:*}
    PORT=${SERVER#*:}

    mysql -h${HOST} -u${USER} -p${PASS} -P${PORT} -e "show databases;" >/dev/null 2>&1

    if [ $? -ne 0 ]; then
        echo "MySQL ${HOST}:${PORT} is down"
        exit 1
    fi
done
echo "All Mysql servers are OK"
exit 0
