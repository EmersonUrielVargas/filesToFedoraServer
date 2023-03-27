#!/bin/bash
#Script to generate a backuo of a database

#echo "Generating a backup of the automation database"
sqlfile="/home/evarg22/Documentos/Documents/Backup/bu_auto_`date '+%Y%m%d_%H%M%S'`.sql" 
logfile="/home/evarg22/Documentos/Documents/Backup/log_`date '+%Y%m%d_%H%M%S'`.txt" 
emails="/home/evarg22/Documentos/Documents/Backup/emails.csv"
credentials="/home/evarg22/Documentos/Documents/Backup/credentials.csv"

echo $sqlfile
echo $logfile

mysqldump world > $sqlfile
more /var/log/syslog | grep db_backup > $logfile



python3 /home/evarg22/Documentos/Documents/Backup/mail.py $logfile $sqlfile $emails $credentials

