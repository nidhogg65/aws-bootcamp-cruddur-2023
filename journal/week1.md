# Week 1 — App Containerization

## Technical Tasks

### 1. Containerize Application
Cruddur application consists of backend-flask and frontend-react-js parts. To containerize the app we need to add respective Dockefiles to backend and frontend directories.

Backend

```
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

Frontend

```
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

Once the Dockerfiles are added, we need to run the containers, but before that images for those containers must be built.
To do that we need to run the following commands:

```
docker build -t  backend-flask ./backend-flask
docker build -t frontend-react-js ./frontend-react-js
```

Then run the containers from the created images:

```
docker run --rm -p 4567:4567 -d -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
docker run --rm -p 3000:3000 -d frontend-react-js
```

To be able to communicate with the app we also need to open frontend and backend ports in gitpod.


## Documented a new notifications endpoint using openAPI.
## Implemented the notifications functionality on backend and frontend sides and ensured that it works.
## Added a local dynamodb to docker compose file, run create table script using AWS CLI thereby ensuring it works.
## Added a postgresql to docker compose file, installed a postgresql client into gitpod and managed to enter the postgresql using the client as well as shell. 

## Technical Tasks

### 1. Push and tag a image to DockerHub
https://hub.docker.com/repositories/nidhogg65
![image](https://user-images.githubusercontent.com/25799157/220741412-052f83b7-b832-4b67-8a6b-1269d7de05aa.png)

### 2.Run the containers on a local machine
![image](https://user-images.githubusercontent.com/25799157/220694440-e4e70196-acff-4817-a40f-b429e78dbd4c.png)

### 3. Implement healthcheck endpoint in Cruddur backend and setup healthcheck in docker compose
To make sure that the application running inside the container is healthy, we need to modify `docker-compose.yaml` file and add healthcheck mechanism for a service.
In my case, I added it for backend service.

```
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    image: nidhogg65/cruddur-backend-flask:1.1
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
    healthcheck:
      test: ["CMD-SHELL", "curl -f $${BACKEND_URL}/api/healthcheck || exit 1"]
      interval: 10s
      retries: 5
      start_period: 30s
      timeout: 5s
```

Since the `test` command, which sends a HTTP request to backend service from the same container, requires curl installed in the container, I had to modify docker image of `backend-flask` too.

```
RUN apt-get update && apt-get install -y curl && apt-get clean
```
A very important fact is that healthcheck request is sent to a new healthcheck endpoint I've implemented in the backend service

```
@app.route("/api/healthcheck", methods=['GET'])
def healthcheck():
    data = []
    return data, 200
```

After running the application containers, we can see after 30 sec (start_period) that `cruddur-backend-flask` is healthy.

![image](https://user-images.githubusercontent.com/25799157/221034332-68502ce5-c184-4370-ac28-0df9ef3df99a.png)

### 4. Use docker files best practices 

#### If Possible, Avoid Multiple Compose Files for Different Environments
The approach of having multiple compose files can cause issues as it is manual and error-prone when reapplying all modifications from one environment to another.
As a rule, you should always try to keep only a single Docker Compose file for all environments.

For these cases, you can use the docker-compose.override.yml file. As its name implies, the override file will contain configuration overrides for existing or entirely new services in your docker-compose.yaml file.

To follow this best practice I created `docker-compose.override.yml` for my `local machine` (outside gitpod) environment.
That file contains some overridden settings which is used in local environment such as backend and frontend URLs.

That file is not supposed to be commited (it must be added in .gitignore), but I added it for a demonstration purpose only. This is a part of the file where I've overridden FRONTEND_URL, BACKEND_URL and REACT_APP_BACKEND_URL.
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

### 5. Create EC2 instance and install docker on it
Create EC2 instance

![image](https://user-images.githubusercontent.com/25799157/221187537-0129fcc9-a9b4-4c70-93ed-932e3a877771.png)

Install docker on it

![image](https://user-images.githubusercontent.com/25799157/221182168-b29f6596-11cc-41ba-ac3e-b5aa43d3b8be.png)

Pull the tagged image from my repository

![image](https://user-images.githubusercontent.com/25799157/221182679-c14d87ef-b6c1-4827-94c3-a433ca123c60.png)

Run the container 

![image](https://user-images.githubusercontent.com/25799157/221186975-4c14dba3-05fd-47de-a0e5-c92d51102d2e.png)

 

