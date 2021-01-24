# Personal site
CV page & notes manager.

## Prerequisites
* Python 3.6+
* Flask 1.1.1+
* PostgreSQL

## Getting started
First, rename example.secrets to .secrets & set your values.  
Then run using docker:
```sh
docker-compose up
```

## Development
Install postgresql or do not if you're going to use SQLite.
```sh
sudo apt install postgresql
```
Install python packages:
```sh
git clone https://github.com/KazakovDenis/MyBlog.git
cd MyBlog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/prod.txt
```
Prepare the database:
```sh
make init_app
```
Then run the server and visit http://localhost:8000:
```sh
make run
```

## Usage
Login to the admin panel using **admin@admin.com / admin** credentials.  
