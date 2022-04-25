# AI Server - Frontend

## Starting server in development
```
./start
```

Add the correct permissions to the file, if required: `chmod +x start`

## Starting server in production

### Configurations

Make configurations in the file `settings.py`

### Start command

```
pm2 start "npm run production" --name frontend
pm2 save
```

### Monitoring the started server

```
pm2 logs backend
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