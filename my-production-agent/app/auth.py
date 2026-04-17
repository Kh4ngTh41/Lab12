from fastapi import Header, HTTPException

API_KEYS = {
    "user1-secret-key": "user_001",
    "user2-secret-key": "user_002",
    "admin-secret-key": "admin_001",
}


def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Verify API key từ header.
    Returns user_id nếu hợp lệ.
    Raises HTTPException(401) nếu sai.
    """
    if x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return API_KEYS[x_api_key]
