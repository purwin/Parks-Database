# Parks Database
This project is a web database used for tracking public art projects. Check out the web app [here](https://nyc-parks-db.herokuapp.com/).

## Built With...
* [Flask](https://palletsprojects.com/p/flask/) -- Python web framework
  * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) -- SQL database ORM
  * [Flask-Login](https://flask-login.readthedocs.io/en/latest/) -- User session management
  * [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) -- Database migrations
  * [Flask-WTF](https://github.com/lepture/flask-wtf) -- Secure form handling
  * [Flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman) -- HTTPS Security
* [PostgreSQL](https://www.postgresql.org/) -- Database storage
* JavaScript

## Getting Started
This'll get you a copy of the project running on your local machine for development and testing.

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

## Project Structure
```
Parks-Database
│
├── /app/                 # Web app dir
│   ├── /add_models/      # Add records to DB scripts
│   ├── forms.py          # Created form classes
│   ├── model_import.py   # Import route functions
│   ├── parks_db.py       # Database model classes
│   ├── /static/          # Web page dir
│   │   ├── /img/         # App imgs
│   │   ├── /js/          # JS dir
│   │   │   ├── /dist/    # Bundled, minified JS files
│   │   │   └── /src/     # Source JS files
|   |   |
│   │   └── /style/       # [S]CSS dir
│   │       ├── /dist/    # Bundled, minified CSS files
│   │       └── /src/     # Source SASS files
│   │   
│   ├── /templates/       # HTML templates
│   ├── users.py          # User classes
│   └── views.py          # Site routes
│
├── config.py             # Environment config file
├── /migrations/          # DB migration dir
├── package-lock.json     # NPM lock file
├── package.json          # Node Package list
├── parks.db              # Database file
├── postcss.config.js     # PostCSS config file
├── Procfile              # App process file
├── requirements.txt      # App requirements file
├── run.py                # App run file
├── runtime.txt           # Python version declaration
├── /tests/               # Route/model test files
└── webpack.config.js     # Webpack config file
```

## Site Structure
```
Index
│
├── /exhibitions/         # Exhibitions landing page
│   ├── /create/          # Create new exhibition page [POST]
│   └── /#/               # Individual exhibition page
│       ├── /edit/        # Edit exhibition page [POST]
│       └── /delete/      # Delete exhibition page [GET/POST]
│
├── /parks/               # Parks landing page
│   ├── /create/          # Create new park page [POST]
│   └── /#/               # Individual park page
│       ├── /edit/        # Edit park page [POST]
│       └── /delete/      # Delete park page [GET/POST]
│
├── /artists/             # Artists landing page
│   ├── /create/          # Create new artist page [POST]
│   └── /#/               # Individual artist page
│       ├── /edit/        # Edit artist page [POST]
│       └── /delete/      # Delete artist page [GET/POST]
│
├── /artworks/            # Artworks landing page
│   ├── /create/          # Create new artwork page [POST]
│   └── /#/               # Individual artwork page
│       ├── /edit/        # Edit artwork page [POST]
│       └── /delete/      # Delete artwork page [GET/POST]
│
├── /orgs/                # Organizations landing page
│   ├── /create/          # Create new organization page [POST]
│   └── /#/               # Individual organization page
│       ├── /edit/        # Edit organization page [POST]
│       └── /delete/      # Delete organization page [GET/POST]
│
├── /import/              # Import records via CSV files
│
├── /create/              # Create a new individual record
```

## Contribute
Reach out if you're interested in helping!

## License
This project is totally open source, licensed under the [MIT License](LICENSE.md).

## Acknowledgments
* [NYC Open Data](https://opendata.cityofnewyork.us) and its [Directory of Parks](https://data.cityofnewyork.us/Recreation/Directory-of-Parks/79me-a7rs)