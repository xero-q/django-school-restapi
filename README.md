### Django project with Django Rest Framework for School App

#### Steps to run the project:
- Install Docker and Docker Compose
- Create a file `.env` in the root folder and set the following environment variables:
    - `DB_DATABASE`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_PORT`
    
- Run these commands:
```sh
docker-compose build
docker-compose up
```
- To stop the project, run:
```sh
docker-compose down
```

