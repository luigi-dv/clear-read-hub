# Use the official Python image from the Docker Hub
FROM python:3.11

# Create a group and user
RUN groupadd -g 10999 app && useradd -r -u 10999 -g app app

# Create the working directory (and set it as the working directory)
WORKDIR /home/app

# Install dependencies
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /var/lib/apt/lists/*

# Switch to the app user
USER app

# Copy the source module & configuration file, service router module & files, application, domain, and infrastructure modules & files, service main file, and the service entrypoint script
COPY --chown=app:app src /home/app/src
COPY --chown=app:app main.py /home/app/main.py
COPY --chown=app:app entrypoint.sh /home/app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /home/app/entrypoint.sh

# Expose port
EXPOSE 8000

# Set the entrypoint script to initiate the container
ENTRYPOINT ["/home/app/entrypoint.sh"]