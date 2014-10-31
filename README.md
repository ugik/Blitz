Blitz
=====

This is the website code for Blitz (Blitz.us).

Blitz.us is a website for personal trainers to train a group of clients and individual clients online.
A trainer recruits a number of clients to follow his/her workout plan, loggin their workouts, socializing with other people working out with that trainer, having a mobile experience that helps them stay on track with workouts. Clients record workouts for their trainer and other group members to view. Trainers can create new programs and manage clients in a variety of plans.

This repository contains the code for Blitz.us as well as scripts necessary to maintain and deploy the site.

Getting Started
===============

### Prerequisites

Developers are expected to be using Pip/Virtualenv.
So, after you clone the repository, create a virtualenv and run `pip install -r requirements.txt`.

### Settings

Any django settings that differ between development and production are contained in `local_settings.py`.
Before you create any code, rename `blitz/RENAME_TO_local_settings.py` to `blitz/local_settings.py`.

### Test environment

For development, Blitz contains a full mock environment - a set of trainers, each with a set of clients.
This data is **not** loaded from a fixture - it is dynamically generated.
To initialize (or reset) the test environment, run:

    sh rebuild.sh

Start the development server, and log in with the following logins:

* email: `amare@example.com`; password: `asdf` (this is a mock client)
* email: `ct@example.com`; password: `asdf` (this is a mock trainer)

### Running tests

Selenium test scripts are in `base/tests/*.py` and run from command line. Database is copied to backup prior to tests and restored upon completion.

`bash runTests.sh`
`bash runTests.sh TestBasic`
`bash runTests.sh TestCreditcards`

### EC2 instance

Please read EC2start.sh and EC2update.sh carefully to understand what is applied to ec2 deployments.

An Ubuntu ec2 instance is formed with `bash EC2start.sh` with public DNS as parameter, this will copy the essential files needed to setup the instance, with `bash EC2setup.sh` ON THE REMOTE SERVER. 
NOTE: prior to running EC2setup.sh, fill out the environment vars at the top of the script. The ec2.pem key is above the Blitz directory structure.

The remote ec2 instance is updated with `bash EC2update.sh` script with public DNS parameter. This rsync's all necessary files and resets Apache. adding a 'migrate' parameter will force deployment server database migration.

### Automated tasks

Celery wrapped in SupervisorD tasks are in `base/tasks.py`, these involve automated email notifications, daily usage digest to team@blitz.us as well as regular backup copy to backup server.

### Backup server

A backup server whose public DNS address is specified in `backup.sh` will receive a SQLdump and a tar file containing all usermedia (user supplied images), as part of a regularly scheduled task. See `base/tasks.py` for details. The backup server will have a replica of the data and media as of the last backup.


