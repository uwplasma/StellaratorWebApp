The folder Stellarator_webapp is for my initial deployment of the web application

query_stellarators.py is the python script for the application I demonstrated in the meeting that day

good_data.sql is the Mysql database that is used by the python script

Note: I have not updated the python script with the updated Mysql database, right now, it still uses the Sqlite toy database which I have not attached. However, I will make that update very soon in the following few days.

Folder Structure


/flask-stellarator|
├── /static
│   └── styles.css     # Contains basic custom styles for the app
│
├── /templates
│   └── index.html     # Contains the main HTML page with Bootstrap
│
├── __init__.py        # Initializes the Flask app
│
└── routes.py          # Defines routes (URLs) and renders HTML pages
File Explanations

__init__.py

This file sets up the Flask application. It is in the app directory.

Purpose: It creates the Flask app instance and imports routes from the routes.py file.
Flask Setup: By creating the app instance, Flask knows how to handle web requests and route them to specific views.
routes.py

Purpose: Defines the route (URL) for the homepage /. When a user visits this URL, the index() function renders index.html from the templates folder.




