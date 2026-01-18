from fastapi import Header, HTTPException
from jose import jwt
from config import CLERK_JWT_PUBLIC_KEY


def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(
            token,
            CLERK_JWT_PUBLIC_KEY,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )

        # Prefer custom claim
        return payload.get("user_id") or payload["sub"]

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
