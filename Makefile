PYTHON=python3
PIP=pip3

# Define variables
BACKEND_VENV_DIR = venv_backend
BACKEND_PATH = webapp/backend
BACKEND_SRC = main.py

FOLDER_SRC=src
APP_ENTRYPOINT=$(FOLDER_SRC)/main.py

help: ## Prints these help pages
	$(info Commands available:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

setup-webservers: ## Setups web servers (both frontend and backend)
	pip3 install -r webapp/backend/requirements.txt --break-system-packages
	cd webapp/frontend && npm install

run-webservers: ## Runs the web servers (both frontend and backend) or restarts them if they were already running
	cd webapp/frontend && pm2 restart frontend || pm2 start "npm run production" --name frontend
	cd webapp/backend && pm2 restart backend || pm2 start "python3 main.py" --name backend
	pm2 save

run-docker-utility: ## Runs the Docker backend utility which starts, stops and restart containers
	cd webapp/backend && pm2 restart backendDockerUtil || pm2 start "python3 dockerUtil.py" --name backendDockerUtil
	pm2 save

view-logs: ## View log entries for started servers (pm2)
	pm2 logs

stop-servers: ## Stops the frontend, backend and docker utility servers (pm2)
	pm2 stop all

run-webservers-dev: # ...
	cd webapp/backend && python3 main.py

run-dev-backend-docker-utility: # ...
	cd webapp/backend && python3 dockerUtil.py

setup-production-webservers:
	echo "Implement..."

setup-production-docker-utility:
	echo "Implement..."

run-production-docker-utility:
	echo "Implement..."

# setup-frontend?
run-dev-frontend: # ...
	cd webapp/frontend && npm run serve



# OLD STUFF; REMOVE LATER

run: ## Run the code
	@$(PYTHON) $(APP_ENTRYPOINT)

test: ## Run tests in the tests/ folder. Outputs HTML results in folder htmlcov/
	$(PYTEST) -vv --cov=src --cov-report html
	$(PYTEST) -vv --cov=src

doc: ## Output pdoc HTML code documentation into folder docs/
	rm -rf ./docs
	PYTHONPATH="." pdoc $(FOLDER_SRC)/* -o docs --docformat google

clean: ## Remove all automatically generated files and folders
	rm -rf docs/
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm .coverage
	rm -rf __pycache__

install-deps: ## Install all required pip packages
	$(PIP) install -r requirements.txt