# AI Server - Frontend

## Settings File

The settings file should be first created in order to start working with the project. File should be created in location ``webapp/frontend/src/AppSettings.js``. Below is an example of this file:

```javascript
 var AppSettings = {};

AppSettings.General = {
  // Email address of the contact person
  contactEmail: "Email address of the contact person",
  // Name of the app
  appName: "Name of the app",
  // Timezone for the frontend
  timezone: "Europe/Helsinki", // https://day.js.org/docs/en/timezone/timezone
}

AppSettings.Login = {
  // Description text to the login page (can be empty)
  loginText: "",
  // Overrides the text Username on the login form. Default: Username
  usernameField: "",
  // Overrides the text Password on the login form. Default: Password
  passwordField: ""
}

AppSettings.APIServer = {
  // URL pointing to your API Server (with trailing slash)
  baseAddress: "http://localhost:8000/api/",
}

// Pre-set settings for the app, no need to modify these
AppSettings.APIServer.user = {}
AppSettings.APIServer.reservation = {}
let baseUrl = AppSettings.APIServer.baseAddress
let baseUserUrl = baseUrl + "user/"
AppSettings.APIServer.user.login = baseUserUrl + "login"
AppSettings.APIServer.user.check_token = baseUserUrl + "check_token"
let baseReservationUrl = baseUrl + "reservation/"
AppSettings.APIServer.reservation.get_available_hardware = baseReservationUrl + "get_available_hardware"
AppSettings.APIServer.reservation.get_current_reservations = baseReservationUrl + "get_current_reservations"
AppSettings.APIServer.reservation.create_reservation = baseReservationUrl + "create_reservation"
AppSettings.APIServer.reservation.get_own_reservations = baseReservationUrl + "get_own_reservations"
AppSettings.APIServer.reservation.cancel_reservation = baseReservationUrl + "cancel_reservation"

export default AppSettings;
```

## Requirements

You need to at least have the following software installed:

- ``NPM``
- ``NodeJS``

## Starting server in development

First, to install the npm packages:
```
npm install
```

Then:
```
./start
```

The server will start by default in port **8080**

Add the correct permissions to the file, if required: `chmod +x start`

## Starting server in production

### Requirements

- ``pm2`` process manager

Note that after installing ``pm2`` you should also run the command ``pm2 startup`` to start pm2 on system reboot.

### Configurations

Make configurations in the file `src/AppSettings.js`

### Start command

```
pm2 start "npm run production" --name frontend
pm2 save
```

### Monitoring the started server

```
pm2 logs frontend
```

Or to monitor the resource usage:

```
pm2 monit
```
