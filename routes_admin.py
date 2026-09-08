from fastapi import APIRouter

from db import get_connection

router = APIRouter()


# VULN: broken-access-control — admin endpoint has zero authentication or
# authorization checks; any anonymous caller can dump every user, including
# plaintext passwords.
@router.get("/admin/users")
def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, password, role, created_at FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "email": r[1], "password": r[2], "role": r[3], "created_at": str(r[4])} for r in rows]


# VULN: broken-access-control — no auth check, PLUS
# VULN: sql-injection — `status` is concatenated raw into the WHERE clause.
@router.get("/admin/orders")
def list_orders(status: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT id, buyer_id, product_id, quantity, status, created_at FROM orders"
    if status:
        query += f" WHERE status = '{status}'"
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "buyer_id": r[1], "product_id": r[2], "quantity": r[3], "status": r[4], "created_at": str(r[5])}
        for r in rows
    ]
