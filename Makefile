VENV := venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python

BOLD := \033[1m
GREEN := \033[32M
YELLOW := \033[33M

compile: ##Compile requirements.txt from requirements.in
	@echo -e "$(BOLD)$(YELLOW)[ Compiling 'requirements.in' into 'requirements.txt'... ]$(RESET)"
	@$(PYTHON) -m piptools compile --resolver=backtracking --upgrade
	@echo ""
	@echo -e "$(BOLD)$(GREEN)[ All done!]$(RESET)"

sync:  ## Sync virtualenv packages with requirements.txt
	@echo -e "$(BOLD)$(YELLOW)[ Synchronizing virtual environment with requirements.txt... ]$(RESET)"
	$(PYTHON) -m piptools sync
	@echo ""
	@echo -e "$(BOLD)$(GREEN)[ All done! ]$(RESET)"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DJANGO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

migrations:  ## Make migrations for all apps
	$(PYTHON) manage.py makemigrations

migrate:  ## Run migrations for all apps
	$(PYTHON) manage.py migrate

checkmigrations:  ## Check migrations without running them
	$(PYTHON) manage.py makemigrations --check --no-input --dry-run

superuser:  ## Create a super user
	$(PYTHON) manage.py createsuperuser

run:  ## Run the Django server
	$(PYTHON) manage.py runserver

statics:  ## Collect statics (for production)
	$(PYTHON) manage.py collectstatic

clearcache:
	$(PYTHON) manage.py shell \
	--command="from django.core.cache import cache; cache.clear()"
