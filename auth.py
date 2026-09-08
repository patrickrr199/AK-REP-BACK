import time

import jwt

from config import JWT_ALGORITHM, JWT_SECRET


# VULN: no-token-expiration — tokens are minted with no "exp" claim, so they
# are valid forever once issued.
def create_token(user_id: int, role: str) -> str:
    payload = {"sub": user_id, "role": role, "iat": int(time.time())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# VULN: insecure-jwt-verification — signature verification is disabled, so
# any caller can forge a token (e.g. {"sub": 1, "role": "admin"}) and it will
# be accepted as-is, including tokens signed with "alg": "none".
def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except Exception:
        return {}
