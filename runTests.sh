#!/bin/bash

# basic test harness
# bash runTests.sh          //runs all tests in base
# bash runTests.sh foo      //runs all tests in base.foo
# bash runTests.sh dev      //copies test db for test development
#
echo "Run Tests..."
if [[ "$1" == "" ]]
	then 
            echo "database backup..."
            cp -v blitz/database.sqlite blitz/database.backup
            cp -v blitz/database.test blitz/database.sqlite
            ./manage.py test base
    elif [[ "$1" != "dev" ]] 
        then
            echo "database backup..."
            cp -v blitz/database.sqlite blitz/database.backup
            cp -v blitz/database.test blitz/database.sqlite
            ./manage.py test base."$1"
    elif [[ "$1" == "dev" ]] 
        then
            echo "test database..."
            cp -v blitz/database.test blitz/database.sqlite
fi

if [[ "$1" != "dev" ]]
    then echo "database restore..."
         cp -v blitz/database.backup blitz/database.sqlite
    else echo "selenium dev mode..."
fi

