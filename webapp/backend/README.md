# AI Server - Backend

Backend server for AI Docker server reservation software, written in Python 3. FastAPI is being used for the API implementation.

## Settings File

The settings file should be first created to start working on the project. The file should be created in the location ``webapp/backend/settings.json``. An example settings file with comments can be found at ``webapp/backend/settings_example.json``.

## Requirements

The following software needs to be installed to run the server:

- ``Python 3``
- ``pip``

## Starting server in development

> It is recommended to run the software in virtual environment.

First, install the pip packages written in the ``requirements.txt`` file (you only need to do this once, or after more requirements have been added):

```
pip install -r requirements.txt
```

Then, to install the ``python-ldap`` package, on Ubuntu you have to run ``apt install python3-ldap``, but on other operating systems you have to run: ``pip3 install python-ldap``.

After that, the server can be started by using the pre-made start script:

```
./start
```

Also – add the correct permissions to the file, if required: `chmod +x start`

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

Or to monitor resource usage:

```
pm2 monit
```

## Settings

All the main settings are located in file `settings.json`. If ``app.addTestDataInDevelopment`` in ``settings.json`` file is set to true, test data will be added as a starting point.

### Default Credentials

Default admin and a regular user are added as a starting point when adding test data and password logins are the way to log in.

**Credentials:**

```
username: aiserveradmin@samk.fi
password: test
```

```
username: aiserveruser@samk.fi
password: test
```

## Specific Details

### Login & Token

Login uses oAuth2 standards. Login creates a bearer token used for all methods meant only for logged-in users.

The endpoint for login is (send the data in POST form data, using username and password):

```
/api/login
```

And endpoint for checking the current token is (send the data in the bearer authentication header):

```
/api/check_token
```

### Timezones & Timestamps

All DateTimes, Dates and Timestamps stored in the database should be stored in UTC + 0 format. Using this, it can be ensured that the times are always right.