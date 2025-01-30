from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from config import SECRET, ALGORITHM







def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=30)) -> str:
    to_encode: dict = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET, ALGORITHM)

