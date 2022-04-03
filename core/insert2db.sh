#!/bin/bash

exe_secelt(){
#cript_dir=$(cd $(dirname $0);pwd)
HOST_NAME="10.22.86.17";
PORT="3306";
USER_NAME="crm";
PASS_WORD="Sunline_123";
DBNAME="sunline_resume";
TABLE_NAME1="base_info_result";
TABLE_NAME2="edu_exp_info_result";
TABLE_NAME3="proj_exp_info_result";
TABLE_NAME4="work_exp_info_result";
HOST=$1;
ignore='"';
script_dir=$(cd $(dirname $0);pwd);
dir=$(dirname $script_dir);
dir2=${dir}"/result/";
insert_base="load data local infile '${dir2}base_info_result.csv' into table ${TABLE_NAME1} fields terminated by ',' optionally enclosed by '${ignore}' lines terminated by '\n' ignore 1 lines";
insert_edu="load data local infile '${dir2}edu_exp_info_result.csv' into table ${TABLE_NAME2} fields terminated by ',' optionally enclosed by '${ignore}' lines terminated by '\n' ignore 1 lines";
insert_proj="load data local infile '${dir2}proj_exp_info_result.csv' into table ${TABLE_NAME3} fields terminated by ',' optionally enclosed by '${ignore}' lines terminated by '\n' ignore 1 lines";
insert_work="load data local infile '${dir2}work_exp_info_result.csv' into table ${TABLE_NAME4} fields terminated by ',' optionally enclosed by '${ignore}' lines terminated by '\n' ignore 1 lines";
mysql -h${HOST_NAME} -P${PORT} -u${USER_NAME} -D ${DBNAME} -p${PASS_WORD} -e "${insert_base}"
mysql -h${HOST_NAME} -P${PORT} -u${USER_NAME} -D ${DBNAME} -p${PASS_WORD} -e "${insert_edu}"
mysql -h${HOST_NAME} -P${PORT} -u${USER_NAME} -D ${DBNAME} -p${PASS_WORD} -e "${insert_proj}"
mysql -h${HOST_NAME} -P${PORT} -u${USER_NAME} -D ${DBNAME} -p${PASS_WORD} -e "${insert_work}"
exit;
}
HOST=$1;
exe_secelt "$HOST"

