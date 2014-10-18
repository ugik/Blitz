#!/bin/bash
project='Blitz'
echo "updating EC2 instance..."

rsync -avC -e "ssh -i ~/Downloads/ec2.pem" /home/gk/Blitz/ ubuntu@"$1":/home/ubuntu/Blitz --exclude 'usermedia' --exclude 'collected_static' --exclude 'migrations' --exclude 'bin/*' --exclude 'lib/*' --exclude '.Python' --exclude 'local_settings.*' --exclude 'database.*' --exclude '.git' --exclude '.sass-cache' --exclude '*.*~' --exclude 'logs' --delete
ssh -i ~/Downloads/ec2.pem ubuntu@$1 sudo service apache2 restart

# bash EC2update.sh ec2-54-213-239-72.us-west-2.compute.amazonaws.com
