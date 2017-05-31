# Wasp
A simple Flask webapp with catalog-like functionality for performing basic CRUD operations for data and Images, API endpoints and Google Account login authetication via Oauth2. Built using SQLAlchemy, sqlite3, OAuth2(Google) with simple CSFR protection for CRUD operations

## Working and Output
This app creates framework with following functionalities
- User Login/Logout Authentication via Google accounts using Oauth2
- CRUD for Categories
- CRUD for individual Items
- CRUD for Images 
- Like/Unlike Items (via Ajax)
- CSFR protection for CRUD operations
- API endpoints 


## Requirements
- Python 2.7 Environment
- flask
- flask_sqlalchemy
- jQuery v3.1.1
- Bootstrap

## Files & folders
- wasp : Outermost folder(root) contains app folder (wasp), app info folder (wasp.egg-info), setup file(setup.py) and manifest (MANIFEST.in)
- wasp.egg-info : This contains App packaging information and requirement
- wasp(app folder) : App files
	- media : contains and stores images used for the app
	- static : contains html, css(bootstrap files + custom 'main.css') and js(bootstrap and jquery files + custom 'helper.js')folders
	- models : contains database model classes
	- templates : html template files used for the app
	- views : contains view files with API and endpoints 
- static folder : This and its subfolders contains all static files used in project(css,js etc)
- templates folder : Contains all the templates that are used for this project(used through jinja2)
- models folder : Python package that holds all the model definition files
- handlers folder : Python package that holds all the handler files and endpoints functions (including API endpoints)

## Usage and installation
- This App is built on a prebuilt vagrant virtual environment with all dependenicies installed provided by udacity. If you want to install on your local machine. Please install following
	- flask
	- flask_sqlalchemy
- Clone/download the repo to your machine
- cd in to the repo root folder
``` cd wasp ```
- Set environment variable and turn debugging on(if required)
	-``` export FLASK_APP=wasp ```
	- ``` export FLASK_DEBUG=true ```
- If running for first time on outside vagrant environment, you need to initiate the db
	- mention your path like so ```engine = create_engine('sqlite:////vagrant/wasp/wasp/wasp.db', convert_unicode=True)``` in database.py file
	- while on root folder. open python shell ```python```
	- ``` from wasp.database import init_db ```
	- ``` init_db() ```
	- exit python shell

- Run the app 
	-``` flask run --host=0.0.0.0 ```
	-App runs on port 5000
	- If you are not on vagrant environment, set your host to your localhost ip (eg: flask run --host=127.0.0.0 )
- App can accessed by going to 'http://localhost:5000' on your browser


## Debugging 
- If you make some changes and flask gives error along the lines of 'not able to find app named wasp'. do the following
	- It is likely be some error while importing new files, to find exact issue
		- On root folder, open python shell. ``` python ```
		- ``` import wasp ```
		- python will print out the errors. Fix it and run flask app again