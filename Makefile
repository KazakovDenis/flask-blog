MANAGER=python3 -m manage
MIGRATE_DIR=blog/migrations

# should be equivalent to config.py vars
PUBLIC_DIR=public
VOLUME_DIR=public/volume

all:
	@echo "Use 'make help' to get targets"

help:
	@grep "^#? " [Mm]akefile

#? -------------------------------- DEVELOPMENT --------------------------------
#? gun:       Run gunicorn
gun:
	gunicorn blog.wsgi:app --log-file=- -c configs/guniconf.py

#? run:       Run flask development server
run:
	$(MANAGER) runserver -p 8000 -h 127.0.0.1

#? migrate:   Create migrations
migrate:
	$(MANAGER) db migrate -d $(MIGRATE_DIR)

#? upgrade:   Apply migrations
upgrade:
	$(MANAGER) db upgrade -d $(MIGRATE_DIR)

#? %:         Execute flask-script command: make shell, make "db downgrade", etc.
%:
	$(MANAGER) $@

#? ---------------------------------- TESTING ----------------------------------
#? test:      Run unit tests
test:
	python3 -m pytest -v tests

#? cover:     Run code test coverage measurement
cover:
	python3 -m coverage run
	- python3 -m coverage report
	- python3 -m coverage html

#? ----------------------- FOR DOCKER CONTAINER PURPOSES -----------------------
#? collect:   Collect all static files into one directory
collect:
	find . -type d -name flask_admin -exec cp -R {}/static ${VOLUME_DIR}/admin \;
	find . -type d -name flask_admin -exec cp -R {}/templates ${VOLUME_DIR}/admin \;

#? publish:   Copy static files and templates into a volume
publish: collect
	cp -R ${PUBLIC_DIR}/templates ${PUBLIC_DIR}/static ${PUBLIC_DIR}/uploads ${VOLUME_DIR}

#? prod:      make publish & run gunicorn
prod: publish
	gunicorn blog.wsgi:app -c guniconf.py
