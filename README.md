# Docker Web Reservation Tool

With this Web app, users can reserve Docker containers with hardware resources needed for their projects. Includes login integration to LDAP systems and plain password logins.

Originally created in Satakunta University of Applied Sciences to give AI students a solution to handle their AI calculating in a dedicated server.

TODO: couple pictures of the system here

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