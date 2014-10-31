#!/bin/bash
FILE=~/backup.server

if [ -f $FILE ];
then
   echo "Reloading..."
mysql -uroot -pmysql  -e "show databases" | grep -v Database | grep -v mysql| grep -v information_schema| grep -v test | gawk '{print "drop database " $1 ";"}' | mysql -uroot -pmysql
mysql -uroot -pmysql < backup/home/ubuntu/Blitz/blitz/usermedia/database.sql

else
   echo "Not a backup system."
fi


