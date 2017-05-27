# library.kdhx.org

## Setting Up a Development Environment

### Project and depdendencies

Install [Miniconda 3](https://conda.io/miniconda.html)

From the project root, install dependencies:

```nohighlight
$ conda env create -f environment.yml
```

Activate the environment:

```nohighlight
$ source activate library.kdhx.org
```

### Setting up a database

- `$ createdb library_kdhx_org`
- `> CREATE ROLE library WITH LOGIN PASSWORD 'independentmusicplayshere';`
- `> GRANT ALL PRIVILEGES ON DATABASE library_kdhx_org TO library;`
- `> ALTER USER library CREATEDB;`

### Setting up Oauth2

TODO

### Running the application

Run the development app server:

```nohighlight
$ python manage.py runserver
```

## Updating environment.yml

```nohighlight
$ conda env export > environment.yml
```