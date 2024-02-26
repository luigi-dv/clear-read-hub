# Azurite External Service
This module is responsible for the Azurite external service.

## Usage
```bash
# Build the docker container
docker build -t my_azurite .
# Run the docker container
docker run -d -p 10000:10000 -p 10001:10001 -p 10002:10002 my_azurite
```

## Configuration
The Azurite external service can be configured using the following environment variables:

- `AZURITE_ACCOUNT_NAME`: The name of the account. Default: `devstoreaccount1`
- `AZURITE_ACCOUNT_KEY`: The account key. Default: `Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==`
- `AZURITE_BLOB_ENDPOINT`: The blob endpoint. Default: `http://
- `AZURITE_QUEUE_ENDPOINT`: The queue endpoint. Default: `http://