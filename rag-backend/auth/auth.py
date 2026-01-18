from fastapi import Header, HTTPException
from typing import Optional

def get_current_user(
    authorization: Optional[str] = Header(None),
) -> str:
    """
    Temporary auth stub.
    Later you can verify Clerk JWT properly.
    """

    if not authorization:
        return "anonymous"

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.replace("Bearer ", "")

    return "clerk_user"
