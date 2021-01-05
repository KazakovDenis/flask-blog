# Flask manager
MANAGER=python3 -m manage
MIGRATE_DIR=blog/migrations

all:
	@echo "Use 'make' for simple commands such as 'make shell' or in a string for complex: 'make \"runserver -p 8000\"'"

gun:
	gunicorn blog.wsgi:app --log-file=- -c configs/guniconf.py

run:
	$(MANAGER) runserver -p 8000 -h 127.0.0.1

migrate:
	$(MANAGER) db migrate -d $(MIGRATE_DIR)

upgrade:
	$(MANAGER) db upgrade -d $(MIGRATE_DIR)

%:
	$(MANAGER) $@

cover:
	python3 -m coverage run
	- python3 -m coverage report
	- python3 -m coverage html

test:
	python3 -m pytest -v tests
