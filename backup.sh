cd ~/backup
mysqldump --all-databases --single-transaction --user=root -pmysql > database.sql
mv database.sql ~/Blitz/blitz/usermedia
tar -czf usermedia.tar.gz ~/Blitz/blitz/usermedia

scp -i ../backup.pem usermedia.tar.gz ubuntu@ec2-54-201-238-160.us-west-2.compute.amazonaws.com:backup/usermedia.tar.gz
ssh -i ../backup.pem ubuntu@ec2-54-201-238-160.us-west-2.compute.amazonaws.com bash reload.sh
exit



