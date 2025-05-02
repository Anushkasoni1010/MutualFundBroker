from datetime import datetime, timezone, timedelta
from pytz import UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import secret_key, algo, access_token_expire_minutes
import jwt

# Secret key for signing JWTs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta if expires_delta else timedelta(minutes=int(access_token_expire_minutes)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token creation failed: {str(e)}"
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_email =  payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Token payload invalid: Missing user identifier.")
        return user_email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token is invalid.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token processing error: {str(e)}")

