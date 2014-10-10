#!/bin/bash
project='Blitz'
echo "updating EC2 instance..."
git remote remove $project.com
git remote add $project.com ssh://ubuntu@"$1"/home/ubuntu/$project.com
ssh-agent bash -c 'ssh-add ~/Downloads/ec2.pem; git push '$project.com' +master:refs/heads/master'
#ssh -i ~/Downloads/ec2.pem ubuntu@"$1" sudo python $project/manage.py migrate
ssh -i ~/Downloads/ec2.pem ubuntu@"$1" sudo service apache2 restart

# bash EC2update.sh ec2-54-213-239-72.us-west-2.compute.amazonaws.com
