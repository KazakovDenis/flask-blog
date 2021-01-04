# Personal site
CV page & notes manager.

## Prerequisites
* Python 3.6+
* Flask 1.1.1+

## Getting started
First of all rename example.env to .env & set your secrets.  

### Using Docker
```sh
$ docker-compose up
```
### In the local env
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
pip install -r requirements/production.txt
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
Enter the admin panel with next credentials: admin@admin.com / admin  
