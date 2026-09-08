from fastapi import APIRouter, Request

from auth import create_token
from db import get_connection

router = APIRouter()


@router.post("/auth/register")
async def register(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")  # VULN: plaintext-password — stored with no hashing

    conn = get_connection()
    cur = conn.cursor()
    # VULN: sql-injection — user input concatenated directly into the query
    query = f"INSERT INTO users (email, password, role) VALUES ('{email}', '{password}', 'customer') RETURNING id"
    cur.execute(query)
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": user_id, "email": email}


@router.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    conn = get_connection()
    cur = conn.cursor()
    # VULN: sql-injection — classic auth-bypassable query built with an f-string,
    # e.g. email = "admin@example.com' -- " bypasses the password check entirely.
    query = f"SELECT id, email, role FROM users WHERE email='{email}' AND password='{password}'"
    cur.execute(query)
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {"error": "invalid credentials"}

    user_id, user_email, role = row
    token = create_token(user_id, role)

    # VULN: sensitive-data-logging — plaintext credentials and the issued
    # token are printed to stdout.
    print(f"[LOGIN] email={email} password={password} token={token}")

    return {"token": token, "user": {"id": user_id, "email": user_email, "role": role}}
