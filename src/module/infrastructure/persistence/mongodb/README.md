# MongoDB Docker Setup

This repository contains a Dockerfile for creating a Docker image with MongoDB Community Server.

## Prerequisites

- Docker installed on your machine.

## Setting Up User and Password
The Dockerfile sets up a user and password for MongoDB using environment variables. Replace `clearreadhub` and `root` in the Dockerfile with your desired username and password.
Then, you can connect to your MongoDB instance from your application environment file changing the `MONGODB_INITDB_ROOT_USERNAME` and `MONGODB_INITDB_ROOT_PASSWORD` environment variables.

```dotenv
# MongoDB
MONGODB_INITDB_ROOT_HOST=localhost
MONGODB_INITDB_ROOT_USERNAME=clearreadhub
MONGODB_INITDB_ROOT_PASSWORD=root
MONGODB_DATABASE_NAME=clearreadhub
```

## Building the Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t my-mongodb .
```
Replace my-mongodb with your preferred image name.

## Running the Docker Container
To run the Docker container, use the following command:
```bash
docker run -p 27017:27017 -d my-mongodb
```
This command maps the container’s port 27017 to your host’s port 27017, allowing you to connect to the MongoDB server running inside the Docker container from your host machine.

## Connecting to MongoDB
Once the Docker container is running, you can connect to MongoDB on localhost port 27017.

## Security
Remember to always handle your data with care and ensure it is securely stored and transmitted.

## Support
If you have any questions or need further assistance, feel free to raise an issue in this repository.