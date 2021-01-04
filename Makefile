# Flask manager
MANAGER=python3 -m blog.manage

all:
	@echo "Use 'make' for simple commands such as 'make shell' or in a string for complex: 'make \"runserver -p 8000\"'"

run:
	$(MANAGER) runserver -p 8000 -h 127.0.0.1

migrate:
	$(MANAGER) db migrate -d blog/migrations

%:
	$(MANAGER) $@
