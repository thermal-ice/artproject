# artproject

A website made in collaboration with a friend for her art project. 

Link: http://firstartproject.ue.r.appspot.com/home

About page: http://firstartproject.ue.r.appspot.com/about

To install: Set a python virtual environment, install all dependencies from requirements.txt, configure a google sheets file and get the creds.json file from it. Let's be honest, you're probably not gonna install this if you're reading this message.


TODO: Clean up code. Figure out how to use a proper database. Implement input sanitization/ basic security so that someone can't delete a crap ton of stuff from the sheets file at will.

V 2.1:
Gcloud can't write files to project directory, so tried switching to GCloud MySQL database. Didn't work properly (actually hard), so switched to google sheets as a database instead. Now it read/writes messages correctly. 

V 2.0: 
Added SQlite database and a reset log page. Now shouldn't be resetting messages every few hours/days. 
Reset log page: http://firstartproject.ue.r.appspot.com/resetTimes


V 1.0: 
Added main functionalities of the web app, including writing and reading messages.
