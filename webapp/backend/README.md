# AI Server - Backend

Backend server for AI Docker server reservation software, written in Python 3. FastAPI is being used for the API implementation.

## Settings File

The settings file should be first created in order to start working with the project. File should be created in location ``webapp/backend/settings.json``. Below is an example of this file:

```json
{
  "app": {
    "name": "SAMK AI Server",
    "logoUrl": "/static/logos/logo.png",
    "host": "127.0.0.1",
    "url": "http://localhost",
    "port": 8000,
    "production": false,
    "addTestDataInDevelopment": true
  },
  "login": {
    "loginType": "password",
    "useWhitelist": false
  },
  "session": {
    "timeoutMinutes": 1440
  },
  "database": {
    "engineUri": "sqlite+pysqlite:///",
    "filePath": "aiserver.db",
    "debugPrinting": false
  }
}
```

### Host

**Setting**: ``app.host``

**Description**: IP address or domain name of your server. Web server will be bound to this address.

### URL

**Setting**: ``app.url``

**Description**: URL address to your server (without trailing slash).

### Port

**Setting**: ``app.port``

**Description**: Port to be used.

### Production

**Setting**: ``app.production``

**Description**: When running the server in production, set ``app.production`` to ``true`` so that no additional debug printing will occur in the server console.

### Add Test Data

**Setting**: ``app.addTestDataInDevelopment``

**Description**: When running the server in development mode and ``app.addTestDataInDevelopment`` is set to ``true``, the app will add some testing credentials, containers, hardware and other data. Have a look at the file ``routes/api.py`` for more reference on this.

### Login Type

**Setting**: ``login.loginType``

**Description**: ``login.loginType`` can be either ``password`` or ``LDAP``. Read below for more information about these options.

#### Password

By setting the ``login.loginType`` to ``password``, login will be done using the ``User`` database. If utilizing this feature, check the file ``admin.py`` for example on how to add users with a password.

#### LDAP

By setting the ``login.loginType`` to ``LDAP``, external LDAP or LDAPS can be used to login user against. If using this login type, some additional information will also be required. Below is an example of this additional information:

```json
  "login": {
    "loginType": "LDAP",
    "ldap": {
      "url": "ldaps://url",
      "usernameFormat": "{username}@ad.local",
      "passwordFormat": "{password}",
      "ldapDomain": "dc=ad,dc=local",
      "searchMethod": "(sAMAccountName={username})",
      "accountField": "sAMAccountName",
      "emailField": "mail"
    }
  },
```

### Login Whitelisting

**Setting**: ``login.useWhitelist``

**Description**: By setting ``login.useWhitelist`` to ``true``, only users that exist in the table ``UserWhitelist`` can login. If utilizing this feature, check the file ``admin.py`` for example on how to whitelist user(s). Whitelisting occurs by user email address.

### Session Timeout

**Setting**: ``session.timeoutMinutes``

**Description**: ``session.timeoutMinutes`` determines how long will logged-in user stay logged in (in minutes). This is set to 1440 minutes by default which means 24 hours.

## Requirements

The following software needs to be installed to run the server:

- ``Python 3``
- ``pip``

## Starting server in development
```
./start
```

Add the correct permissions to the file, if required: `chmod +x start`

## Starting server in production

### Requirements

- ``NPM``
- ``pm2`` process manager

### Configurations

Make configurations in the file `settings.py`

### Start command

Starting the backend server:

```
pm2 start "python3 main.py" --name frontend
pm2 save
```

Starting the Docker helper:

```
pm2 start "python3 dockerUtil.py" --name backendDockerUtil
pm2 save
```

### Monitoring the started server

```
pm2 logs backend
```

```
pm2 logs backendDockerUtil
```

Or to monitor the resource usage:

```
pm2 monit
```

## Settings

All the main settings are located in file `settings.json`.

## Specific Details

### Login & Token

Login uses oAuth2 standards. Login creates a bearer token used for all methods meant only for logged-in users.

Endpoint for login is (send the data in POST form data, using username and password):

```
/api/login
```

And endpoint for checking the current token is (send the data in bearer authentication header):

```
/api/check_token
```

### Timezones & Timestamps

All DateTimes, Dates and Timestamps stored in the database should be stored in UTC + 0 format. This way we can ensure that the times are always right.
