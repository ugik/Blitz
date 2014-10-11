#!/bin/bash
echo "setup EC2 instance..."

# setup vars
github_password='GITHUB PASSWORD'
email_password='EMAIL PASSWORD'
secret_key='SECRET_KEY'
ip_address='0.0.0.0'

repo='ugik'
project='Blitz'
project_app=$project"/blitz"

# update Ubuntu instance
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install python-pip
sudo apt-get -y install git-core

#setup and install PIL w/ZIP support:
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg62 libjpeg62-dev
sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

#setup and install Pillow w/ZIP support:
sudo pip install Pillow

#grab requirements
sudo pip install -r requirements.txt
sudo pip install six --upgrade
sudo pip install django-bootstrap-toolkit

# setup remaining .LAMP elements
sudo apt-get -y install apache2 libapache2-mod-wsgi
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password mysql'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password mysql'
sudo apt-get -y install mysql-server python-mysqldb

# django rdbms privileges
cd ~
mysql -u root -pmysql -e "create database data; GRANT ALL PRIVILEGES ON data.* TO django@localhost IDENTIFIED BY 'django'"

# grab repo
cd /home/ubuntu
sudo git clone https://$repo:$github_password@github.com/$repo/$project.git

# set privs
cd /home/ubuntu/$project_app
sudo chmod o+wx -R usermedia

# add host to /etc/hosts
sudo sed -i -e '1i'$ip_address' '$project'\' /etc/hosts

# copy WSGI files
cd /home/ubuntu
sudo cp $project/WSGI/project.wsgi ./$project.wsgi
sudo cp $project/WSGI/project.conf /etc/apache2/sites-available/$project.conf

# instance env vars
export EMAIL_PASSWORD='$email_password'
sudo echo "export EMAIL_PASSWORD='$email_password'" >> ~/.bashrc
sudo echo "export SECRET_KEY='$secret_key'" >> ~/.bashrc
source ~/.bashrc

# sample data
cd /home/ubuntu/$project
bash rebuild.sh

# apache2 available sites
sudo a2dissite 000-default
sudo a2ensite $project.conf

# static files
sudo chown ubuntu:ubuntu /home/ubuntu/$project_app
cd /home/ubuntu/$project
python manage.py collectstatic --noinput
sudo /etc/init.d/apache2 restart

# setup remote git repo and hooks
cd /home/ubuntu
sudo mkdir $project.com
cd $project.com
sudo git init --bare
sudo chown ubuntu:ubuntu -R objects
sudo chown ubuntu:ubuntu -R refs
cd hooks

sudo touch post-receive
sudo chmod o+wrx post-receive
sudo echo '#!/bin/sh' >> post-receive
sudo echo "DESTINATION=/home/ubuntu/"$project >> post-receive
sudo echo "GIT_WORK_TREE=/home/ubuntu/"$project".com/" >> post-receive
sudo echo "export GIT_WORK_TREE" >> post-receive
sudo echo "git checkout -f" >> post-receive
sudo echo "rsync -az $GIT_WORK_TREE $DESTINATION --exclude 'usermedia' --delete" >> post-receive
cd ~


# references:
# Ubuntu 14.x remote LAMP setup: http://nickpolet.com/blog/1/
# locale LAMP setup: http://www.lleess.com/2013/05/install-django-on-apache-server-with.html#.UwavkDddV38
# http://cuppster.com/2011/01/30/using-git-to-remotely-install-website-updates/

