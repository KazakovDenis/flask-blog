# Flask manager
MANAGER=python3 -m manage
MIGRATE_DIR=blog/migrations

# should be equivalent to config.py vars
PUBLIC_DIR=blog/public
VOLUME_DIR=blog/public/volume

all:
	@echo "Use 'make' for simple commands such as 'make shell' or in a string for complex: 'make \"runserver -p 8000\"'"

# -------------------------------- DEVELOPMENT -------------------------------- #
# Run production server
gun:
	gunicorn blog.wsgi:app --log-file=- -c configs/guniconf.py

# Run development server
run:
	$(MANAGER) runserver -p 8000 -h 127.0.0.1

# Create migrations
migrate:
	$(MANAGER) db migrate -d $(MIGRATE_DIR)

# Apply migrations
upgrade:
	$(MANAGER) db upgrade -d $(MIGRATE_DIR)

# Execute Flask manager command
%:
	$(MANAGER) $@

# ---------------------------------- TESTING ---------------------------------- #
test:
	python3 -m pytest -v tests

cover:
	python3 -m coverage run
	- python3 -m coverage report
	- python3 -m coverage html

# ----------------------- FOR DOCKER CONTAINER PURPOSES ----------------------- #
publish:
	cp -R $(PUBLIC_DIR)/templates $(PUBLIC_DIR)/static $(VOLUME_DIR)

prod: publish
	gunicorn blog.wsgi:app -c guniconf.py
