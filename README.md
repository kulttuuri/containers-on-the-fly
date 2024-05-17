# Containers on the Fly
> Instant Up. Timely Down. Simple web-based Docker container reservation platform.

<img width="500" alt="image 7" src="https://github.com/Satakunnan-ammattikorkeakoulu/containers-on-the-fly/assets/3810422/61a9d8d4-c788-4528-a245-3930543a7a34">

## Description

With this Web app, users permitted to access the app can easily reserve Docker containers with hardware resources needed for their projects. The user can select the start and end time for the container reservation. Multiple servers can be integrated for reservations.

Users can login with username & password combination, or through LDAP. Includes also admin-level management tools in the web app.

Originally created in Satakunta University of Applied Sciences to give AI students a solution to handle their AI calculating in a dedicated server.

## Screenshots

![image](https://user-images.githubusercontent.com/3810422/197523647-d603e763-fbf8-42cc-b211-1ca1343e2550.png)

![image](https://user-images.githubusercontent.com/3810422/197523756-0b1d79fb-64ed-4a86-a0a6-aed6a0757dab.png)

![image](https://user-images.githubusercontent.com/3810422/197523917-237ddd05-d35c-4d76-917d-963e60144598.png)

![image](https://user-images.githubusercontent.com/3810422/197524065-1a6b3452-e449-458c-a703-edd699a43f3b.png)

## Software Architecture

![image](/additional_documentation/architecture.png)

By default, the Main Server contains the web servers, database, and local docker registry. These services can also be distributed to other servers, if required to.

The Container Servers run, stop, and restart the containers reserved. Container server can also be distributed to the Main Server. It is possible to scale the service to multiple servers by adding more servers running the Container Server.

## Technologies Used

The app is split into two projects: frontend and backend. The frontend can be located from `webapp/frontend` and backend from `webapp/backend`. Both the frontend and backend will run on different ports. The backend also includes a separate script for starting and stopping the reserved containers.

### Frontend

The frontend has been developed using Vue 2.

### Backend

The backend has been developed using Python 3, SQLAlchemy and FastAPI.

The backend also includes a tool called `dockerUtils.py` that handles starting and stopping the reserved containers.

## Getting Started

This web app should be run in the host computer where you want to be able to reserve these Docker containers. It is recommended to only use the computer for this specific software for security reasons.

Both the `webapp/frontend` and `webapp/backend` folders contain individual setup instructions for settings up those systems. It is recommended to first setup the frontend part running on a computer and then after that the backend part.
