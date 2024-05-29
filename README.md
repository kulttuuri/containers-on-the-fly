# Containers on the Fly
> Instant Up. Timely Down. Simple web-based Docker container reservation platform.

<img width="500" alt="image 7" src="https://github.com/Satakunnan-ammattikorkeakoulu/containers-on-the-fly/assets/3810422/61a9d8d4-c788-4528-a245-3930543a7a34">

## Description

With this Web app, users permitted to access the app can easily reserve Docker containers with hardware resources needed for their projects. The user can select the start and end time for the container reservation. Multiple servers can be integrated for reservations.

Users can login with username & password combination, or through LDAP. Includes also admin-level management tools in the web app.

Originally created in Satakunta University of Applied Sciences to give AI students a solution to handle their AI calculating in a dedicated server.

## Screenshots

![image](https://user-images.githubusercontent.com/3810422/197523647-d603e763-fbf8-42cc-b211-1ca1343e2550.png)

![image](https://user-images.githubusercontent.com/3810422/197523917-237ddd05-d35c-4d76-917d-963e60144598.png)

![image](https://user-images.githubusercontent.com/3810422/197524065-1a6b3452-e449-458c-a703-edd699a43f3b.png)

![image](https://github.com/Satakunnan-ammattikorkeakoulu/containers-on-the-fly/assets/3810422/b548cb69-7226-4d14-8363-ddcdb6dc244b)


## Getting Started

The installation consists of two parts and one additional part:
1. [Install the Main Server](#automatic-installation-main-server), which contains the web servers (web interface), database, and local docker registry. All Docker images will be added to the local docker registry and other servers can then utilize these images from this main server.
2. [Install the Container Server](#automatic-installation-container-server) from which the virtual Docker reservations can be made. This container server script handles starting, stopping, and restarting container reservations on the server. The container server can reside at the same location as the Main Server, and/or in multiple other servers from which users can reserve containers.
3. (Optional) [Secure the server by closing any additional ports](#securing-the-server).

### Automatic Installation: Main Server

> Heads up! The automatic installation script for the **main server** only works with Ubuntu Linux 22.04. It is HIGHLY RECOMMENDED to use a fresh Ubuntu installation, due to various software being installed and configured. For any other operating system, the installation procedure is required to be [conducted manually](#manual-installation-main-server).

Before proceeding, make sure you are logged in as the user with which you want to setup the Main Server. The user should have sudo permissions. For example: `containeruser`. Root user is not recommended to be used.

The installation procedure of the Main Server (web servers, database, local Docker registry) is as follows:

#### Copy Configurations

Copy the settings files from `user_config/examples` to `user_config` folder. If you do not require an SSL certificate (your web interface is accessed using the HTTP protocol), then copy the `nginx_settings.conf` file. If you plan to use an SSL certificate (your web server will be accessed using the HTTPS protocol) then copy the file `nginx_settings_ssl.conf`.

#### Create Configurations

After copying the files, make configurations to the files. The files to configure are:

- `user_config/settings`: The main settings file. You should at least review and configure the settings here.
- `user_config/backend_settings.json`: Settings for the backend (web api) of the web interface. Would be good to review this file for any extra configurations.
- `user_config/frontend_settings.js`: Settings for the frontend of the web interface. Might not require any extra configurations.
- `user_config/nginx_settings.conf`: Contains the configurations for the Nginx proxy server. Does not require any extra configurations.

If you plan to use LDAP login (it is highly recommended to set it up only after you have verified that the default server installation and login works first), then you need to run these extra commands:

on Ubuntu you have to run ``sudo apt install python3-ldap``, but on other operating systems you have to run: ``pip3 install python-ldap``.

#### Setup the Main Server

After the configurations are ready, start setting up the main server and it's dependencies with:

```bash
sudo make setup-main-server
```

Default admin and a regular user accounts are added to the system automatically, if the backend setting addTestDataInDevelopment is set to true (true by default). The accounts are as follows:

```
username: admin@foo.com
password: test
```

```
username: user@foo.com
password: test
```

#### Start the Main Server

After the main server setup is complete, run all the main server dependencies with:

```bash
make start-main-server
```

That's it! Now you should be able to access the web interface using a browser. There will be more information printed on your console after running the `make start-main-server` command. If the servers crash or something happens, then you should only need to run the `make start-main-server` command again.

### Automatic Installation: Container Server

> The automatic installation of the Container Server has been at least tested with with Ubuntu Linux and MacOS and should work with other Unix systems. If you encounter any problems in the installation, then review the make commands to run from the Makefile and manually run the commands.

Before proceeding, make sure you are logged in as the user with which you want to setup the Main Server. The user should have sudo permissions. For example: `containeruser`. Root user is not recommended to be used.

The installation procedure of the Container Server is as follows:

#### Copy Configurations

Copy the settings files `user_config/examples/settings` and `user_config/examples/backend_settings.json` to the `user_config` folder.

#### Create Configurations

After copying the files, make configurations to the files. The files to configure are:

- `user_config/settings`: The main settings file. You should at least review and configure the settings here.
- `user_config/backend_settings.json`: Settings for the backend (web api) of the web interface. Would be good to review this file for any extra configurations.

#### Setup the Docker Utility

After the configurations are ready, set up the docker utility with:

```bash
make setup-docker-utility
```

#### Start Docker Utility

After the setup is complete, run the Docker utility with:

```bash
make start-docker-utility
```

That's it! If the container crashes or something happens to the utility, then you should only need to run the `make start-docker-utility` command again.

### Manual Installation: Main Server

The installation procedure of the Main Server (web servers, database, local Docker registry) is as follows:

##### Install Dependencies

Install:
- Python
- Pip
- Nginx
- MariaDB
- pm2 Process Manager
- NPM & NodeJS (version 20)

##### Configure the Dependencies

Set MariaDB to launch at startup.

In MariaDB, create a database and a user that has access to it.

Disable the default nginx site:
```
sudo rm /etc/nginx/sites-enabled/default
```

Add custom nginx configurations to the nginx file:
```
sudo sed -i "/http {/a \\    include /path/to/your/user_config/nginx_settings.conf;" /path/to/your/user_config/nginx_settings.conf
```

##### Copy Configurations

Copy the settings files from `user_config/examples` to `user_config` folder. If you do not require an SSL certificate (your web interface is accessed using the HTTP protocol), then copy the `nginx_settings.conf` file. If you plan to use an SSL certificate (your web server will be accessed using the HTTPS protocol) then copy the file `nginx_settings_ssl.conf`.

##### Create Configurations

After copying the files, make configurations to the files. The files to configure are:

- `user_config/settings`: The main settings file. You should at least review and configure the settings here.
- `user_config/backend_settings.json`: Settings for the backend (web api) of the web interface. Would be good to review this file for any extra configurations.
- `user_config/frontend_settings.js`: Settings for the frontend of the web interface. Might not require any extra configurations.
- `user_config/nginx_settings.conf`: Contains the configurations for the Nginx proxy server. Does not require any extra configurations.

##### Start the Servers

After the setup is complete, run the main server dependencies with:

```bash
make start-main-server
```

That's it! Now you should be able to access the web interface using a browser. There will be more information printed on your console after running the `make start-main-server` command.

## Additional Tasks

### Securing the Server
You should definitely close all unnecessary incoming ports from the server and only allow what you wish. The example ufw configuration below achieves this:

```bash
sudo ufw reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 2000:3000/tcp
sudo ufw allow 2000:3000/udp
sudo ufw enable
sudo ufw status
```

The port range 2000-3000 set above can be set to your own range. This setting can be set in the ``user_config/settings`` file.

Note that if you want to set-up an additional container server, you need to also open the incoming docker registry port (defaults to 5000), which can be set in the ``user_config/settings` file.

### Adding Images to Containers
Using the admin interface, user can add new containers. These containers still require an image added to it manually.

The process of adding an image that users can reserve is as follows:

1. Create the image in the admin interface. This can be done using the **Containers** section.
2. Create a new container and make a note of the image name. By default, you should add at least the SSH port for the image (service name: SSH, port: 22). Make the image public in order for users to reserve it.
3. Create image for the container in the server where you have the **Main Server** installed. Copy the file ``DockerfileContainerExample`` to some safe location and make your own modifications to the image as required.
4. In the same folder where you copied the file ``DockerfileContainerExample``, run these two commands to build the image and push it to local Docker registry, replacing the **IMAGENAME** with the name of your image in the admin web interface:

```bash
docker build -t localhost:5000/IMAGENAME:latest -f DockerfileContainerExample .
docker push localhost:5000/IMAGENAME:latest
```

And that's it. Now you should be able to reserve the container!

## Technical Details

![image](/additional_documentation/architecture.png)

The app is split into two projects: frontend and backend. The frontend can be located from `webapp/frontend` and backend from `webapp/backend`. Both the frontend and backend will run on different ports. The backend also includes a separate script for starting and stopping the reserved containers, called `dockerUtil.py`.

### Frontend

The frontend has been developed using Vue 2.

### Backend

The backend has been developed using Python 3, SQLAlchemy and FastAPI.

The backend also includes a tool called `dockerUtils.py` that handles starting and stopping the reserved containers.
