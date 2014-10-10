Blitz
=====

This is the website code for Blitz (Blitz.us).
This particular repository is a development sandbox - we use it to build new features.

FitFlame is a website for personal trainers to train a group of clients online.
A trainer recruits a number of clients to follow his/her workout plan for ~12 weeks.
Clients record workouts for their trainer and other group members to view.
There is also a social feed for clients and trainers to talk about their experiences in the plan.


Getting Started
===============

### Prerequisites

Developers are expected to be using Pip/Virtualenv.
So, after you clone the repository, create a virtualenv and run `pip install -r requirements.txt`.

### Settings

Any django settings that differ between development and production are contained in `local_settings.py`.
Before you create any code, rename `blitz/RENAME_TO_local_settings.py` to `blitz/local_settings.py`.
The defaults will probably work.

### Test environment

For development, Blitz contains a full mock environment - a set of trainers, each with a set of clients.
This data is **not** loaded from a fixture - it is dynamically generated.
To initialize (or reset) the test environment, run:

    sh rebuild.sh

Start the development server, and log in with the following logins:

* email: `amare@example.com`; password: `asdf` (this is a mock client)
* email: `ct@example.com`; password: `asdf` (this is a mock trainer)

### Adding test data

See base/management/commands/setup_new_stuff.py for loading additional test data, specifically new clients for trainers. A group of clients on a program for a trainer is called a 'Flame'.


