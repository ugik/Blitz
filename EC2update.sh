#!/bin/bash
project='Blitz'
echo "updating EC2 instance..."

rsync -avL -e "ssh -i ~/Downloads/ec2.pem" /home/gk/$project/ ubuntu@"$1":/home/ubuntu/$project --exclude 'usermedia' --exclude 'python2.7' --exclude '.Python' --exclude 'local_settings.*' --exclude 'database.*' --delete
ssh -i ~/Downloads/ec2.pem ubuntu@$1 sudo service apache2 restart

# bash EC2update.sh ec2-54-213-239-72.us-west-2.compute.amazonaws.com
