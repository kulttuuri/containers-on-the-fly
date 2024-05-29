#!/bin/bash

######
# This script is used to merge settings from the user_config/settings file to
# user_config/frontend_settings.js and user_config/backend_settings.json files.
######

CURRENT_DIR=$(pwd)

# Load settings
source "$CURRENT_DIR/user_config/settings"

# Function to escape special characters in a variable for use with sed
escape_sed() {
    echo "$1" | sed 's/[\/&]/\\&/g'
}

# Function to perform sed operation
perform_sed() {
    local file=$1
    local search=$2
    local replace=$3
    if sed --version >/dev/null 2>&1; then
        # GNU sed
        sed -i -e "$search" "$file"
    else
        # BSD sed (macOS)
        sed -i '' -e "$search" "$file"
    fi
}

# Timezone
ESCAPED_TIMEZONE=$(escape_sed "$TIMEZONE")
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"timezone\": \).*/\1\"$ESCAPED_TIMEZONE\",/"
perform_sed user_config/frontend_settings.js "s/^\([[:space:]]*timezone: \).*/\1\"$ESCAPED_TIMEZONE\",/"

# Docker Registry Address
ESCAPED_REGISTRY_ADDRESS=$(escape_sed "$DOCKER_REGISTRY_ADDRESS")
ESCAPED_REGISTRY_PORT=$(escape_sed "$DOCKER_REGISTRY_PORT")
ESCAPED_REGISTRY_FULL="${ESCAPED_REGISTRY_ADDRESS}:${ESCAPED_REGISTRY_PORT}"
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"registryAddress\": \).*/\1\"$ESCAPED_REGISTRY_FULL\",/"

# Docker Reservation Start Port
ESCAPED_PORT=$(escape_sed "$DOCKER_RESERVATION_PORT_RANGE_START")
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"port_range_start\": \).*/\1\"$ESCAPED_PORT\",/"

# Docker Reservation End Port
ESCAPED_PORT=$(escape_sed "$DOCKER_RESERVATION_PORT_RANGE_END")
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"port_range_end\": \).*/\1\"$ESCAPED_PORT\",/"

# Server address in frontend settings file
ESCAPED_SERVER_WEB_ADDRESS=$(escape_sed "$SERVER_WEB_ADDRESS")
perform_sed user_config/frontend_settings.js "s/^\([[:space:]]*baseAddress: \).*/\1\"$ESCAPED_SERVER_WEB_ADDRESS\/api\/\",/"

# App name
ESCAPED_APP_NAME=$(escape_sed "$APP_NAME")
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"name\": \).*/\1\"$ESCAPED_APP_NAME\",/"
perform_sed user_config/frontend_settings.js "s/^\([[:space:]]*appName: \).*/\1\"$ESCAPED_APP_NAME\",/"

# Email address
ESCAPED_EMAIL_ADDRESS=$(escape_sed "$CONTACT_EMAIL")
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"helpEmailAddress\": \).*/\1\"$ESCAPED_EMAIL_ADDRESS\"/"
perform_sed user_config/frontend_settings.js "s/^\([[:space:]]*contactEmail: \).*/\1\"$ESCAPED_EMAIL_ADDRESS\",/"

# Database URI
URI="mysql+pymysql://"$MARIADB_DB_USER":"$MARIADB_DB_USER_PASSWORD"@"$MARIADB_SERVER_ADDRESS"/"$MARIADB_DB_NAME
ESCAPED_URI=$(escape_sed "$URI")
perform_sed user_config/backend_settings.json "s/^\([[:space:]]*\"engineUri\": \).*/\1\"$ESCAPED_URI\",/"