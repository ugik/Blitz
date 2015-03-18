#!/bin/bash
project='Blitz'
echo "updating EC2 instance..."

if [[ "$1" == "" ]]
	then echo "usage: bash EC2update.sh {host-name} [migrate]"
    else 

rsync -avC -e "ssh -i ../backup.pem" /home/ugik/Blitz/ ubuntu@"$1":/home/ubuntu/Blitz --exclude 'usermedia' --exclude 'migrations' --exclude 'collected_static' --exclude 'bin/*' --exclude 'lib/*' --exclude '.Python' --exclude 'local_settings.*' --exclude 'database.*' --exclude '.git' --exclude '*.conf' --exclude '.sass-cache' --exclude '*.*~' --exclude 'logs' --delete

    if [[ "$2" != "" ]]
	then echo "migrating schema..."
             ssh -i ../backup.pem ubuntu@$1 $project/manage.py schemamigration base --auto
             ssh -i ../backup.pem ubuntu@$1 $project/manage.py migrate base
             ssh -i ../backup.pem ubuntu@$1 $project/manage.py schemamigration workouts --auto
             ssh -i ../backup.pem ubuntu@$1 $project/manage.py migrate workouts

    fi
    ssh -i ../backup.pem ubuntu@$1 $project/manage.py collectstatic --noinput
    echo "apache graceful restart..."
    ssh -i ../backup.pem ubuntu@$1 sudo apachectl graceful
fi

