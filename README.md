# ChallengeMe

This is the backend for the ChallengeMe application for the Cornell AppDev final hackathon course in Fall 2018

Frontend: https://github.com/seancorc/ChallengeMe 

To set up the backend, first install necessary dependencies

`pip install -r src/requirements.txt`

To run the flask server

`python3 src/routes.py`

The initial database is within the "CHALLENGEME.db" sqlite file. To reset this database, first

`rm CHALLENGEME.db`

then re run the seeder with  

`python3 seed.py`



