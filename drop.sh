# mysql -u root -p
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';

find . -name 'migrations' -type d -exec rm -rf {} +
find . -name '__pycache__' -type d -exec rm -rf {} +

function mysql_call() {
  cmd="$1"
  mysql -h"localhost"  -P"3306"  -u"root" -e "${cmd}" --default-character-set=UTF8
}

db_name="marcovdb"
mysql_call "set global time_zone='+8:00'"
mysql_call "drop database ${db_name};" >/dev/null 2>&1
mysql_call "create database ${db_name} default character set utf8mb4 COLLATE = utf8mb4_unicode_ci;"

