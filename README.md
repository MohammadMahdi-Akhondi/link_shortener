# Link Shortener

this project is a simple link shortener that takes a long URL from user and converts it into a much shorter manageable link.

## Features
- Convert long URLs into short links
- Supports both English and Persian languages.
- Uses two-step verification of the user account using SMS.
- Connected to the payment gateway

## Technologies
- Implemented using [Django framework](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/)
- Utilizes [Celery](https://docs.celeryq.dev/en/stable/) for executing time-consuming tasks asynchronously
- Utilizes [Redis](https://redis.io/) as a cache
- Uses [RabbitMQ](https://www.rabbitmq.com/) as a message broker
- Dockerized project for easy setup and deployment
- Uses [JWT](https://django-rest-framework-simplejwt.readthedocs.io/) to authenticate users
- Tested using TestCase and APIClient

## Usage
1. Clone the project repository:
``` shell
git clone https://github.com/MohammadMahdi-Akhondi/link_shortener.git
cd link_shortener
```

2. Create and edit the configuration file:
``` shell
cp setting-sample.ini setting.ini
nano setting.ini
```
Configure the necessary project settings in this file.

3. Build and launch the Docker environment:
``` shell
docker-compose up --build
```

4. The project is now accessible, and you can open document of project in your browser:
> http://localhost:8000/swagger/

## Requirements
To build and run the project, you need the following dependencies:

- Docker and Docker Compose

if you need to install Docker and Docker Compose, please refer to their official documentation.

## Development and contribution
if you would like to contribute to the development and improvement of this project, you can following these steps:

1. Fork this repository
2. Create a new branch
``` shell
git checkout -b your-feature
```

3. Make your changes and commit them:
``` shell
git commit -m "Add your feature"
``` 

4. push your branch:
``` shell
git push origin your-feature
``` 

5. Create a new Pull Request and explain your changes.

I look forward to your contributions :)
