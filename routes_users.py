from fastapi import APIRouter

from db import get_connection

router = APIRouter()


# VULN: idor — returns any user record, including the plaintext password, by
# id with no authentication or ownership check.
@router.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password, role, created_at FROM users WHERE id = %s", (user_id,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    if not r:
        return {"error": "not found"}
    return {"id": r[0], "email": r[1], "password": r[2], "role": r[3], "created_at": str(r[4])}
