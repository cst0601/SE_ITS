# Issue Tracking System

## To run
1. Download and install MongoDB.
2. Set DB URI at `backend/src/its_model/mongo.py`.
3. run `python src/its_model/mongo.py` to start.

## Line Message Gun
Handles message sent by users via line. \
To get Line user id for further use of the system, type `get id` to ITS Line broadcaster.

This part of the system runs on a seperate machine. \
LMG is currently running on heroku, [portal to machine](https://line-issue-broadcaster.herokuapp.com/) [Note: This page will not show anything worthy.]

### Running LMG
* This subsystem requires SSL enabled connection, SSL connection is not enabled, LMG will not respond to any message sent to it.
* Build a virtualenv and run `pip install -r requirements.txt`
