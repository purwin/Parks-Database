# Parks Database
This project is a web database used for tracking public art projects. Check out the web app [here](https://nyc-parks-db.herokuapp.com/).

## Built With...
* [Flask]() -- Python web framework
  * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) -- 
  * [Flask-Login]() -- User session management
  * [Flask-Migrate]() -- database migrations
  * [Flask-WTF](https://github.com/lepture/flask-wtf) -- 
  * [Flask-talisman]()
* [PostgreSQL](https://www.postgresql.org/) -- Database storage
* JavaScript

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
👉 [Python](https://www.python.org/)  
👉 [Pip](https://pypi.org/project/pip/)  
👉 [Virtualenv](https://virtualenv.pypa.io/en/latest/) & [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/index.html)  
👉 [NPM](https://www.npmjs.com/)

### Install
Clone the app files to your computer
```
$ git clone https://github.com/purwin/Parks-Database.git
$ cd Parks-Database
```

### Setup
Create a virtual environment, then install the required app and node packages:
```
$ mkvirtualenv parks-db
$ workon parks-db
$ pip install -r requirements.txt
$ npm install
```

### Run
Get a dev server up and running on [http://localhost:5000](http://localhost:5000)
```
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
$ flask run
```

### Tests
To test routes and database models, run
```
$ python -m unittest discover -s tests
```

### Migrations
If altering any database models, run the following commands to handle migrations
```
$ flask db migrate
$ flask db upgrade
```
## Database

## Project Structure
```
Parks-Database
│
├── /app/                 # Goalie stat CSV source files
│   ├── /add_models/      #
│   ├── forms.py          # Created form classes
│   ├── model_import.py   #
│   ├── parks_db.py       # Database model classes
│   ├── /static/          #
│   │   ├── /img/         # App imgs
│   │   ├── /js/          # 
│   │   │   ├── /dist/    # Bundled, minified JS files
│   │   │   └── /src/     # Source JS files
|   |   |
│   │   └── /style/       #
│   │       ├── /dist/    # Bundled, minified CSS files
│   │       └── /src/     # Source SASS files
│   │   
│   ├── /templates/       # 
│   ├── users.py          # User classes
│   └── views.py          # Site routes
│
├── config.py             # Environment config file
├── import_parks.py       # Public HTML file/resources
├── /migrations/          # DB migration history
├── package-lock.json     # NPM lock file
├── package.json          # Node Package list
├── parks.db              # Database file
├── postcss.config.js     # Database file
├── Procfile              # App process file
├── requirements.txt      # App requirements file
├── run.py                # App run file
├── runtime.txt           # Database file
├── /tests/               # Route/model test files
└── webpack.config.js     # Webpack config file
```

## Contribute
Reach out if you're interested in helping!

## License
This project is totally open source, licensed under the [MIT License](LICENSE.md).

## Acknowledgments
* [NYC Open Data](https://opendata.cityofnewyork.us) and its [Directory of Parks](https://data.cityofnewyork.us/Recreation/Directory-of-Parks/79me-a7rs)