# Issue Tracking System
ITS(Issue Tracking System) is a web based system for users to create projects and submit issues.

## To run backend
1. Download and install MongoDB.
2. Set DB URI at `backend/src/its_model/mongo.py`.
3. <>
4. run `python app.py` to start.

## Line Message Gun
Handles message sent by users via line. \
To get Line user id for further use of the system, type `get id` to ITS Line broadcaster.

This part of the system runs on a seperate machine. \
LMG is currently running on heroku, [portal to machine](https://line-issue-broadcaster.herokuapp.com/) [Note: This page will not show anything worthy.]

### Running LMG
* This subsystem requires SSL enabled connection, SSL connection is not enabled, LMG will not respond to any message sent to it.
* Setting up secret token and webhook:
    * Folder that saves token and webhook needs to be named as `line_broadcaster/secret_mix`.
    * Files names as `token` and `webhook` needs to be added in the `ecret_mix` folder, and record secret messages in it.
* Build a virtualenv and run `pip install -r requirements.txt`
