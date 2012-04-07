About

This is the code that the team: "Project Badass" submitted for the 2010 McGill codjam.

The McGill codejam is a 48 hour coding competition held yearly at McGill. The teams compete to produce the "best" implementation of the specified program. In 2010 the task was to produce server and visualisation code for a stock exchange system.

"Project Badass" placed third and is composed of:
* alanalynch
* dannenberg
* mcsquiggedy
* StephenHamilton
* tahnok

This was really a learning experience for us. The members of our team each had only a bit of python knowledge, so we were learning the basics as we went. Having learned a lot about coding since, especially higher level project stuff, I am impressed at how much we got right way back when. So I leave this here for historical reasons and hope you enjoy.

Installation

Dependencies
* python2
* python-mysql
* matplotlib
* numpy
* wx-python

Instructions

The code is not terribly easy to set up, as we were setting it up ourselves for the competition. The details on how we went about this are a bit fuzzy now two years later. We are using a MySQL database, which is set up as follows:
    "CREATE DATABASE databasename; GRANT ALL ON databasename.* TO 'newusername'@'localhost' IDENTIFIED BY 'newpassword'; flush privileges;"
Then there may come some fiddling, which is the not easy part. Especially if you want a secure database (because you are not running it on a secure VM like we were) then you would have to fiddle with the code to change the password.

Usage

The program should set up the tables itself. Then you can start it using:
    python gui.py
To make it do anything you then need to start the test client that is supplied in the spec folder and point it to port 30000 on localhost.
