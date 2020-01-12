# Issue Tracking System
ITS(Issue Tracking System) is a web based system for users to create projects and submit issues.

## Build frontend pages
1. Move current working directory to `project/react`
2. Run `npm install` to install required packages.
3. Run `npm run build` to build.

## To run backend
1. Download and install MongoDB.
2. Move current work directory to `backend`
3. Do `pip install -r requirements.txt` to install required packages.
4. Setting up secret mix:
  * Create a folder named `secret_mix` in `project/backend`
  * Create two files in the folder, `token` and `mail_passwd` that contains line token and email password seperately.
5. Set mongo URI by modifying the MONGO_URI variable in `src/its_model/mongo.py`
6. Create root account by issuing command `python src/its_model/mongo.py`.
7. Run `flask run` to start.
8. The default url of the website is 127.0.0.1:5000 (or as shown on console).

## To access system manager page
Sign in as system manager (default:root)
Go to <your url here>/accountmanager

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

## Run Acceptance Test
1. Move current work directory to `at/src` 
2. Run `pip install --upgrade robotframework` 
3. Run `pip install --upgrade robotframework-seleniumlibrary` 
4. Run `pip install --upgrade robotframework-selenium2library` 
5. Download webDriver base on your browser https://selenium.dev/downloads/
6. Move webDriver file to your python folder or add environment variable `Path` 
7. Run `robot <scriptFile.robot>` to run selected script.

### Running backend unit test
1. Move current working directory to `backend`
2. Run `coverage run -m unittest discover` to run unit test
3. Run `coverage result -m` to get the code coverage.
