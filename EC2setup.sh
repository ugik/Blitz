#!/bin/bash
if [ -d "/home/gk" ]; then
  echo "Local setup, exiting..."
  exit
fi

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
sudo apt-get -y install rabbitmq-server
sudo apt-get -y install supervisor
sudo apt-get -y install rpl

#setup and install PIL w/ZIP support:
sudo apt-get -y build-dep python-imaging
sudo apt-get -y install libjpeg62 libjpeg62-dev
sudo apt-get -y install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib

#setup and install Pillow w/ZIP support:
sudo pip install Pillow

#grab requirements
sudo pip install -r requirements.txt
sudo rm -rf /usr/local/lib/python2.7/dist-packages/requests*
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

# set privs for usermedia dirs
cd /home/ubuntu/$project_app
sudo chmod o+wx -R usermedia
cp /home/ubuntu/$project/sample_blitz_program.xls /home/ubuntu/$project_app/usermedia/programs/.

# add host to /etc/hosts
sudo sed -i -e '1i'$ip_address' '$project'\' /etc/hosts

# copy WSGI files
cd /home/ubuntu
sudo cp $project/WSGI/project.wsgi ./$project.wsgi
sudo cp $project/WSGI/project.conf /etc/apache2/sites-available/$project.conf
sudo mkdir backup

# copy SSL certs
sudo mkdir /etc/apache2/ssl
cd /home/ubuntu/$project/ssl
sudo cp blitz_us.crt /etc/apache2/ssl
sudo cp www.blitz.us.key /etc/apache2/ssl
sudo cp COMODORSAAddTrustCA.crt /etc/apache2/ssl
sudo cp blitz_us.ca-bundle /etc/apache2/ssl

# instance env vars
export EMAIL_PASSWORD='$email_password'
sudo echo "export EMAIL_PASSWORD='$email_password'" >> ~/.bashrc
sudo echo "export SECRET_KEY='$secret_key'" >> ~/.bashrc
source ~/.bashrc

# apache2 available sites
sudo a2dissite 000-default
sudo a2ensite $project.conf
sudo a2enmod ssl

# static files
sudo chown ubuntu:ubuntu -R /home/ubuntu/$project
cd /home/ubuntu/$project
python manage.py collectstatic --noinput

# sample data
cd /home/ubuntu/$project
bash rebuild.sh

# supervisord
cd /home/ubuntu/$project
mkdir logs
sudo rpl '*EMAIL_PASSWORD*' $email_password supervisord.conf
sudo rpl '*SECRET_KEY*' $secret_key supervisord.conf
supervisord

cd ~

sudo /etc/init.d/apache2 restart
sudo ps -ef | grep supervisord

# references:
# Ubuntu 14.x remote LAMP setup: http://nickpolet.com/blog/1/
# locale LAMP setup: http://www.lleess.com/2013/05/install-django-on-apache-server-with.html#.UwavkDddV38
# http://www.webforefront.com/django/setupapachewebserverwsgi.html
# http://bixly.com/blog/supervisord-or-how-i-learned-to-stop-worrying-and-um-use-supervisord/

