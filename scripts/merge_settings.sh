#!/bin/sh

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


# IP Address
sed -i.bak "s/^\([[:space:]]*\"host\": \).*/\1\"$SERVER_IP_ADDRESS\",/" user_config/backend_settings.json

# Timezone
ESCAPED_TIMEZONE=$(escape_sed "$TIMEZONE")
sed -i.bak "s/^\([[:space:]]*\"timezone\": \).*/\1\"$ESCAPED_TIMEZONE\",/" user_config/backend_settings.json
sed -i.bak "s/^\([[:space:]]*timezone: \).*/\1\"$ESCAPED_TIMEZONE\",/" user_config/frontend_settings.js

# Server address in frontend settings file
ESCAPED_SERVER_WEB_ADDRESS=$(escape_sed "$SERVER_WEB_ADDRESS")
sed -i.bak "s/^\([[:space:]]*baseAddress: \).*/\1\"$ESCAPED_SERVER_WEB_ADDRESS\/api\/\",/" user_config/frontend_settings.js

# App name
ESCAPED_APP_NAME=$(escape_sed "$APP_NAME")
sed -i.bak "s/^\([[:space:]]*\"name\": \).*/\1\"$APP_NAME\",/" user_config/backend_settings.json
sed -i.bak "s/^\([[:space:]]*appName: \).*/\1\"$APP_NAME\",/" user_config/frontend_settings.js

# Email address
ESCAPED_EMAIL_ADDRESS=$(escape_sed "$CONTACT_EMAIL")
sed -i.bak "s/^\([[:space:]]*\"helpEmailAddress\": \).*/\1\"$ESCAPED_EMAIL_ADDRESS\"/" user_config/backend_settings.json
sed -i.bak "s/^\([[:space:]]*contactEmail: \).*/\1\"$ESCAPED_EMAIL_ADDRESS\",/" user_config/frontend_settings.js

# Database URI
URI="mysql+pymysql://"$MARIADB_DB_USER":"$MARIADB_DB_USER_PASSWORD"@"$MARIADB_SERVER_ADDRESS"/"$MARIADB_DB_NAME
ESCAPED_URI=$(escape_sed "$URI")
sed -i.bak "s/^\([[:space:]]*\"engineUri\": \).*/\1\"$ESCAPED_URI\",/" user_config/backend_settings.json
# "engineUri": mysql+pymysql://root:root@localhost/aiserver
# "engineUri": "mysql+pymysql://root:root@localhost/aiserver",