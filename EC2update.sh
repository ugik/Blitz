#!/bin/bash
project='Blitz'
echo "updating EC2 instance..."

if [[ "$1" == "" ]]
	then echo "usage: bash EC2update.sh {host-name} [migrate] [preview]"
    else 

        if [[ "$2" == "preview" ]] 
        then
              echo "dry-run rsync..."
              rsync -aCi -e "ssh -i ../ec2.pem" /home/ugik/Blitz/ ubuntu@"$1":/home/ubuntu/Blitz --exclude 'usermedia' --exclude 'migrations' --exclude 'collected_static' --exclude 'bin/*' --exclude 'lib/*' --exclude '.Python' --exclude 'local_settings.*' --exclude 'database.*' --exclude '.git' --exclude '*.conf' --exclude '.sass-cache' --exclude '*.*~' --exclude 'logs' --delete --dry-run
        else
              rsync -aCi -e "ssh -i ../ec2.pem" /home/ugik/Blitz/ ubuntu@"$1":/home/ubuntu/Blitz --exclude 'usermedia' --exclude 'migrations' --exclude 'collected_static' --exclude 'bin/*' --exclude 'lib/*' --exclude '.Python' --exclude 'local_settings.*' --exclude 'database.*' --exclude '.git' --exclude '*.conf' --exclude '.sass-cache' --exclude '*.*~' --exclude 'logs' --delete 

           if [[ "$2" != "" ]]
	      then echo "migrating schema..."
                 ssh -i ../ec2.pem ubuntu@$1 $project/manage.py schemamigration base --auto
                 ssh -i ../ec2.pem ubuntu@$1 $project/manage.py migrate base
                 ssh -i ../ec2.pem ubuntu@$1 $project/manage.py schemamigration workouts --auto
                 ssh -i ../ec2.pem ubuntu@$1 $project/manage.py migrate workouts
           fi
        fi

    ssh -i ../ec2.pem ubuntu@$1 $project/manage.py collectstatic --noinput
    echo "apache graceful restart..."
    ssh -i ../ec2.pem ubuntu@$1 sudo apachectl graceful
fi

