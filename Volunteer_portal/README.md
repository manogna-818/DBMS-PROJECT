# System Requirements
You should install and setup PostgreSQL.

# Introduction

The repository contains a web app which is a volunteer. The following
features are supported

1. Adding an activity.
1. Lists all the activities.
1. Delete activities.
1. Lists enrolled activities and applied activites.

# Setting up

1. Open terminal and run command `createdb volunteer` to create the database.  
1. Clone repository
1. Create a virtualenv and activate it
1. Install dependencies using `pip install -r requirements.txt`
1. `export FLASK_APP=volunteer` to set the application
1. `flask initdb` to create the initial database
1. `flask run` to start the app.
