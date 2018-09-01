# library.kdhx.org

## Setting Up a Development Environment

### Project and depdendencies

Install `virtualenv`:

```nohighlight
$ pip install virtualenv
```

Create a new virtual environment, specifying a Python 3.6 binary:

```nohighlight
$ virtualenv -p PATH_TO_PYTHON_36 venv
```

Activate the environment:

```nohighlight
$ source venv/bin/activate
```

From the project root, install dependencies:

```nohighlight
$ pip install -r requirements.txt
```

### Setting Up the Database

- `$ createdb library_kdhx_org`
- `> CREATE ROLE library WITH LOGIN PASSWORD 'independentmusicplayshere';`
- `> GRANT ALL PRIVILEGES ON DATABASE library_kdhx_org TO library;`
- `> ALTER USER library CREATEDB;`

### Setting Up Oauth2

TODO

### Setting Up Elasticsearch

To reindex:

```nohighlight
$ ./manage.py rebuild_index
```

### Running the application

Run the development app server:

```nohighlight
$ python manage.py runserver
```

## Updating requirements.txt

```nohighlight
$ pip freeze > requirements.txt
```

## Importing Data

```nohighlight
$ ./manage.py runscript import_genres
```

To move all albums with a given label ID to another label ID (does not affect additional labels for the given albums):

```nohighlight
$ ./manage.py runscript merge_labels --script-args from_id to_id
```

## Building Static Assets with Webpack

```nohighlight
$ npm run build
```

To build with hot deploy enabled during development:

```nohighlight
$ npm run watch
```