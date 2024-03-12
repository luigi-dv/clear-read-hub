from datetime import datetime, timedelta, timezone

from jose import jwt

from src.service_config import serviceConfig


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        serviceConfig.SERVICE_OAUTH_CLIENT_SECRET,
        algorithm=serviceConfig.SERVICE_OAUTH_ENCODE_ALGORITHM,
    )
    return encoded_jwt
