# Clear Read Hub

[![Clear Read Hub Docker Build](https://github.com/luigi-dv/clear-read-hub/actions/workflows/docker-image.yml/badge.svg)](https://github.com/luigi-dv/clear-read-hub/actions/workflows/docker-image.yml)
[![License](https://black.readthedocs.io/en/stable/_static/license.svg)](https://github.com/luigi-dv/clear-read-hub)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/luigi-dv/clear-read-hub)
 
Clear Read Hub is a microservice architecture application built with FastAPI, following the principles of Domain-Driven Design (DDD).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11
- Pip
- FastAPI
- MongoDB

### Installing

A step by step series of examples that tell you how to get a development environment running.

```bash
# Clone the repository
git clone https://github.com/luigi-dv/clear-read-hub.git

# Navigate into the directory
cd clear-read-hub

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

### Docker

You can also run the application using Docker.

```bash
# Build the image
docker build -t clear-read-hub:latest .
# Run the container
docker run -p 8000:8000 clear-read-hub:latest
# Run the container in detached mode
docker run -d -p 8000:8000 clear-read-hub:latest
 ```

## Running the tests

Explain how to run the automated tests for this system.

## Deployment

Add additional notes about how to deploy this on a live system.

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Python](https://www.python.org/) - The programming language used

## Contributing

Please read [CONTRIBUTING.md](https://github.com/luigi-dv/clear-read-hub/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- [Luigi Davila](https://github.com/luigi-dv)

See also the list of [contributors](https://github.com/luigi-dv/clear-read-hub/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/yourusername/clear-read-hub/blob/main/LICENSE.md) file for details

