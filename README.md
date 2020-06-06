# My personal blog 
To accumulate all the information I could not to remember, want to save at hand and do not want to google.

## Getting started
### Installation
###### [for Debian based]
If you want to use Postgresql:
```sh
$ sudo apt install postgresql
```
Clone the repo and install all dependencies:
```sh
$ git clone https://github.com/KazakovDenis/MyBlog.git
$ pip install -r requirements/production.txt
```
### Configuring
Set environment variables (GH is Github). 

for ~/.bashrc (or ~/.profile):
```
export DB_USER="database_user"
export DB_PASS="database_password"
export FLASK_SECRET="random_string1"
export FLASK_SALT="random_string2"
export GH_SECRET="random_string3"
export GH_REPO_ID="your_repo_id"
```
for supervisor config
```
[program:blog]
environment=
    DB_USER="database_user",
    DB_PASS="database_password",
    FLASK_SECRET="random_string1",
    FLASK_SALT="random_string2",
    GH_SECRET="random_string3",
    GH_REPO_ID="random_string4"
```
Choose SQLite in SQLALCHEMY_DATABASE_URI of "config/config.py" or use PostgresQL.
Look [psycopg2](https://pypi.org/project/psycopg2/) to install the last and then create a database and add a user. 

### Starting
Finally, start the project by executing:
```shell script
$ cd your/app/root/directory/
$ source venv/bin/activate
$ python startproject.py
> Are you sure the database has been created and environment variables are set? [y/n] --> y
$ python3 -m app.manage runserver
```
Visit `127.0.0.1:5000` and log in by using admin@admin.com / admin123.
**Enjoy!**
