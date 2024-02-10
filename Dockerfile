FROM registry.access.redhat.com/ubi8/ubi:latest

ENV PYTHON_VERSION=3.11 \
    PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_NO_CACHE_DIR=off

# Install libraries
RUN yum search odbc
RUN yum search gcc
RUN yum search gcc-c++
RUN yum search python3.11
RUN yum search python3.11-devel
RUN yum search python3.11-pip
RUN yum search msodbcsql18
RUN yum search openssl

# Install required
RUN yum install -y unixODBC unixODBC-devel gcc gcc-c++ python3.11 python3.11-devel python3.11-pip openssl

ADD . /app

# Create a group and user
RUN groupadd -g 10999 app && useradd -r -u 10999 -g app app

# Create the working directory (and set it as the working directory)
RUN mkdir -p /home/app && chown app:app /home/app
WORKDIR /home/app

# Switch to the app user
USER app

# Copy the requirements file to the working directory
COPY --chown=app:app requirements.txt /home/app/

# Install python dependencies
RUN python3 -m pip install --upgrade setuptools pip \
    &&  python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the working directory
COPY --chown=app:app . /home/app/

# Delete files not required
RUN rm Dockerfile && rm requirements.txt

# Copy the tests folder to the working directory
#COPY --chown=app:app test /home/app/test

# Run tests
# RUN python -m unittest discover -s /home/app/test

# Delete directory Test
# RUN rm -r /home/app/test


# Make the entrypoint script executable
RUN chmod +x /home/app/entrypoint.sh

# Expose port
EXPOSE 8000

# Set the entrypoint script to initiate the container
ENTRYPOINT ["/home/app/entrypoint.sh"]
