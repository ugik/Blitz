#!/bin/bash
project='Blitz'
echo "updating EC2 instance..."

rsync -avL -e "ssh -i ~/Downloads/ec2.pem" /home/gk/Blitz/ ubuntu@ec2-54-69-24-164.us-west-2.compute.amazonaws.com:/home/ubuntu/Blitz --exclude 'usermedia' --exclude 'collected_static' --exclude 'python2.7' --exclude '.Python' --exclude 'local_settings.*' --exclude 'database.*' --exclude '.git' --exclude '.sass-cache' --delete
ssh -i ~/Downloads/ec2.pem ubuntu@$1 sudo service apache2 restart

# bash EC2update.sh ec2-54-213-239-72.us-west-2.compute.amazonaws.com
