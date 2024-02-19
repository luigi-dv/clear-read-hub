# Use the latest MongoDB Community Server image
FROM mongodb/mongodb-community-server:latest

# Set environment variables for MongoDB user and password
ENV MONGODB_INITDB_ROOT_USERNAME=admin
ENV MONGODB_INITDB_ROOT_PASSWORD=root

# Expose the MongoDB port
EXPOSE 27017

# Define default command to start MongoDB service
CMD ["mongod"]
