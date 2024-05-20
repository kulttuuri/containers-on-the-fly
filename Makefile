PYTHON=python
PIP=pip

# Define variables
BACKEND_PATH = webapp/backend
BACKEND_SRC = main.py
FOLDER_SRC=src
APP_ENTRYPOINT=$(FOLDER_SRC)/main.py
CONFIG_SETTINGS = "user_config/settings"
CONFIG_BACKEND_SETTINGS = "user_config/backend_settings.json"
CONFIG_FRONTEND_SETTINGS = "user_config/frontend_settings.js"
CONFIG_NGINX_SETTINGS = "user_config/nginx_settings.conf"

GREEN=\033[0;32m
RED=\033[0;31m
RESET=\033[0m

help:
	$(info Make tool for the containers on the fly project.)
	$(info Using this make tool, you can setup and run the services. Commands available:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS=":.* ## "}; {printf "> make %-25s\n%s\n\n", $$1, $$2};'

# Helper targets

verify-all-config-files-exist: # Verify that all configuration files exists in the user_config folder.
	@if [ ! -e $(CONFIG_SETTINGS) ]; then \
		echo "Error: $(CONFIG_SETTINGS) does not exist. Please copy the example settings file from the user_config/examples folder to user_config location and write your own configurations first."; \
		exit 1; \
	fi
	@if [ ! -e $(CONFIG_BACKEND_SETTINGS) ]; then \
		echo "Error: $(CONFIG_BACKEND_SETTINGS) does not exist. Please copy the example settings file from the user_config/examples folder to user_config location and write your own configurations first."; \
		exit 1; \
	fi
	@if [ ! -e $(CONFIG_FRONTEND_SETTINGS) ]; then \
		echo "Error: $(CONFIG_FRONTEND_SETTINGS) does not exist.  Please copy the example settings file from the user_config/examples folder to user_config location and write your own configurations first."; \
		exit 1; \
	fi
	@if [ ! -e $(CONFIG_NGINX_SETTINGS) ]; then \
		echo "Error: $(CONFIG_NGINX_SETTINGS) does not exist.  Please copy the example settings file from the user_config/examples folder to user_config location and write your own configurations first."; \
		exit 1; \
	fi

check-os-ubuntu: # Checks if the operating system is Ubuntu. Stops executing if not.
	@OS_NAME=$$(lsb_release -si 2>/dev/null || echo "Unknown") && \
	if [ "$$OS_NAME" != "Ubuntu" ]; then \
		echo "\n$(RED)Error: This setup script is only compatible with Ubuntu Linux. Please refer to the readme documentation for manual steps. Exiting.$(RESET)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Operating system is Ubuntu Linux. Proceeding with setup.$(RESET)"

# Production targets

setup-webservers: check-os-ubuntu verify-all-config-files-exist ## Installs and configures all dependencies for web servers. Only works on Ubuntu Linux. If using any other operating system, then refer to the readme documentation for manual steps.
	@chmod +x scripts/install_webserver_dependencies.bash
	@./scripts/install_webserver_dependencies.bash
	$(PIP) install -r webapp/backend/requirements.txt
	cd webapp/frontend && npm install
	echo "\n$(GREEN)Setup successful! Now run 'make run-webservers' to start the web servers.\n"

run-webservers: verify-all-config-files-exist ## Runs the web servers or restarts them if started. Nginx is used to create a reverse proxy. pm2 process manager is used to run other servers in the background. 
	# TODO: Move settings from the settings file to backend and frontend settings files.
	
	@cp user_config/backend_settings.json webapp/backend/settings.json
	@cp user_config/frontend_settings.js webapp/frontend/src/AppSettings.js
	@systemctl reload nginx
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
	@chmod +x scripts/install_docker_dependencies.bash
	@./scripts/install_webserver_dependencies.bash
	@pip3 install -r webapp/backend/requirements.txt --break-system-packages
	@echo "$(GREEN)The Docker utility has been setupped.$(RESET)"

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