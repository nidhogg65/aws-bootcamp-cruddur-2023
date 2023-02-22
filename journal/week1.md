# Week 1 — App Containerization

## Containerized Cruddur Application using Dockerfiles and Docker Compose, and ensured that it works in gitpod.
## Documented a new notifications endpoint using openAPI.
## Implemented the notifications functionality on backend and frontend sides and ensured that it works.
## Added a local dynamodb to docker compose file, run create table script using AWS CLI thereby ensuring it works.
## Added a postgresql to docker compose file, installed a postgresql client into gitpod and managed to enter the postgresql using the client as well as shell. 
## Managed to run all the containers locally using locally installed Docker and ensured that Cruddur app works
![image](https://user-images.githubusercontent.com/25799157/220694440-e4e70196-acff-4817-a40f-b429e78dbd4c.png)
## Added docker-compose.override.yml 
That file contains some overridden settings which is used in local environment such as backend and frontend URLs.
That file is not supposed to be commited (it must be added in .gitignore), but I added it for a demonstration purpose only.
```version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "http://localhost:3000"
      BACKEND_URL: "http://localhost:4567"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "http://localhost:4567"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
      ..........................................
```
## Created repositories for frontend and backend images with tags in DockerHub
https://hub.docker.com/repositories/nidhogg65
![image](https://user-images.githubusercontent.com/25799157/220741412-052f83b7-b832-4b67-8a6b-1269d7de05aa.png)


