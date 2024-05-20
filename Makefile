PYTHON=python
PIP=pip

# Define variables
BACKEND_PATH = webapp/backend
BACKEND_SRC = main.py
FOLDER_SRC=src
APP_ENTRYPOINT=$(FOLDER_SRC)/main.py
CONFIG_BACKEND_SETTINGS = "user_config/backend_settings.json"
CONFIG_FRONTEND_SETTINGS = "user_config/frontend_settings.js"
CONFIG_NGINX_SETTINGS = "user_config/nginx_config.json"

GREEN=\033[0;32m
RED=\033[0;31m
RESET=\033[0m

help:
	$(info Make tool for the containers on the fly project.)
	$(info Using this make tool, you can setup and run the services. Commands available:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS=":.* ## "}; {printf "> make %-25s\n%s\n\n", $$1, $$2};'

# Scripts for production

verify-all-config-files-exist:
	@if [ ! -e $(CONFIG_BACKEND_SETTINGS) ]; then \
		echo "Error: $(CONFIG_BACKEND_SETTINGS) does not exist. Please copy the example settings file from the user_config folder to this location and write your own configurations first."; \
		exit 1; \
	fi
	@if [ ! -e $(CONFIG_FRONTEND_SETTINGS) ]; then \
		echo "Error: $(CONFIG_FRONTEND_SETTINGS) does not exist.  Please copy the example settings file from the user_config folder to this location and write your own configurations first."; \
		exit 1; \
	fi
	@if [ ! -e $(CONFIG_NGINX_SETTINGS) ]; then \
		echo "Error: $(CONFIG_NGINX_SETTINGS) does not exist.  Please copy the example settings file from the user_config folder to this location and write your own configurations first."; \
		exit 1; \
	fi

setup-webservers: verify-all-config-files-exist ## Setups the web servers. Run this at least once before calling run-webservers. Installs and configures all required services (like mariadb, nginx, npm, nodejs, python...)
	# TODO: Install NGINX, MariaDB etc...
	pip3 install -r webapp/backend/requirements.txt --break-system-packages
	cd webapp/frontend && npm install

run-webservers: verify-all-config-files-exist ## Runs the web servers or restarts them if started. Nginx is used to create a reverse proxy. pm2 process manager is used to run other servers in the background. 
	@cp user_config/backend_settings.json webapp/backend/settings.json
	@cp user_config/frontend_settings.js webapp/frontend/src/AppSettings.js
	@cd webapp/frontend && pm2 restart frontend 2>/dev/null || pm2 start "npm run production" --name frontend
	@cd webapp/backend && pm2 restart backend 2>/dev/null || pm2 start "python3 main.py" --name backend
	@pm2 save
	@CLIENT_URL=$$(grep '"clientUrl"' user_config/backend_settings.json | sed 's/.*"clientUrl": "\(.*\)".*/\1/') && \
	echo "" && \
	echo "$(GREEN)Web servers (frontend, backend) have been started / restarted!$(RESET)" && \
	echo "Access the launched web interface at: $(GREEN)$$CLIENT_URL$(RESET) (it can take several seconds for the server to launch)" && \
	echo "You can view any logs (errors) using the $(GREEN)make view-logs$(RESET) command."

setup-docker-utility: ## Setups the Docker utility. The Docker utility will start, stop, and restart the containers on this machine. Call 'make run-docker-utility' after setup.
	# Check that the backend settings configuration file exists
	@if [ ! -e $(CONFIG_BACKEND_SETTINGS) ]; then \
		echo "Error: $(CONFIG_BACKEND_SETTINGS) does not exist. This utility uses the $(CONFIG_BACKEND_SETTINGS) file to connect to the database, please configure this file first."; \
		exit 1; \
	fi
	@pip3 install -r webapp/backend/requirements.txt --break-system-packages
	@echo "$(GREEN)The Docker utility has been setupped.$(RESET)"
	# TODO: Other required configurations

run-docker-utility: ## Runs the Docker utility. pm2 process manager is used to run the script in the background.
	@echo "Verifying that connection to the database can be made using the $(CONFIG_BACKEND_SETTINGS) setting engineUri..."
	@CONNECTION_URI=$$(grep '"engineUri"' $(CONFIG_BACKEND_SETTINGS) | sed 's/.*"engineUri": "\(.*\)".*/\1/') && \
	CONNECTION_OK=$$(python scripts/verify_db_connection.py "$$CONNECTION_URI") && \
	if [ "$$CONNECTION_OK" = "CONNECTION_OK" ]; then \
		echo "Connection to the database was successful. Proceeding."; \
	else \
		echo "\n$(RED)Connection to the database could not be established. Please check that you have the $(CONFIG_BACKEND_SETTINGS) setting engineUri properly set and that connection to the database can be made (firewalls etc...).$(RESET)"; \
		exit 1; \
	fi

	@cp user_config/backend_settings.json webapp/backend/settings.json
	@cd webapp/backend && pm2 restart backendDockerUtil 2>/dev/null || pm2 start "python3 dockerUtil.py" --name backendDockerUtil --log-date-format="DD-MM-YYYY HH:mm"
	@pm2 save
	@echo "\n$(GREEN)Docker utility is now running.$(RESET)"
	@echo "Containers will now automatically start, stop, and restart on this server."

logs: ## View log entries for started servers (pm2)
	pm2 logs --lines 300

status: ## Views the status of the started servers (pm2)
	pm2 list

stop-servers: ## Kills (stops) the frontend, backend and docker utility servers (pm2 process manager)
	@-pm2 delete frontend 2>/dev/null || echo "frontend pm2 service was not running. Nothing to stop."
	@-pm2 delete backend 2>/dev/null || echo "backend pm2 service was not running. Nothing to stop."
	@-pm2 delete backendDockerUtil 2>/dev/null || echo "backendDockerUtil pm2 service was not running. Nothing to stop."
	@echo "\n$(GREEN)Servers stopped!$(RESET)"


# Scripts for development

run-dev-frontend:
	cd webapp/frontend && npm run serve

run-dev-backend:
	cd webapp/backend && python3 main.py

run-dev-docker-utility:
	cd webapp/backend && python3 dockerUtil.py