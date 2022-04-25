# AI Server - Frontend

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

- **pm2** process manager
- **NPM**
- **NodeJS**

Note that after installing **pm2** you should also run the command ``pm2 startup`` to start pm2 on system reboot.

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