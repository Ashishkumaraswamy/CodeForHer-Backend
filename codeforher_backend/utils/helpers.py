from fastapi import HTTPException, status

import jwt

from codeforher_backend.models.config import JWTConfig

def raise_service_exception(status: status, details: str):
    raise HTTPException(
        status_code=status,
        detail=details,
    )

def verify_token(jwt_config: JWTConfig, token: str):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, jwt_config.jwt_secret, algorithms=[jwt_config.jwt_algorithm])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except Exception as e:
        print(f"Error verifying token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )