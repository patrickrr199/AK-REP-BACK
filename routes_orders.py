from typing import Optional

from fastapi import APIRouter, Request

from db import get_connection

router = APIRouter()


# VULN: idor — `buyer_id` comes straight from the query string with nothing
# tying it to the authenticated caller, so anyone can list anyone else's
# order history by changing the id (same class as GET /orders/{id} below).
@router.get("/orders")
def list_orders(buyer_id: Optional[int] = None):
    conn = get_connection()
    cur = conn.cursor()
    if buyer_id is not None:
        cur.execute(
            """
            SELECT o.id, o.product_id, p.title, o.quantity, o.status, o.created_at
            FROM orders o JOIN products p ON p.id = o.product_id
            WHERE o.buyer_id = %s
            ORDER BY o.created_at DESC
            """,
            (buyer_id,),
        )
    else:
        cur.execute(
            """
            SELECT o.id, o.product_id, p.title, o.quantity, o.status, o.created_at
            FROM orders o JOIN products p ON p.id = o.product_id
            ORDER BY o.created_at DESC
            """
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "product_id": r[1],
            "product_title": r[2],
            "quantity": r[3],
            "status": r[4],
            "created_at": str(r[5]),
        }
        for r in rows
    ]


@router.post("/orders")
async def create_order(request: Request):
    body = await request.json()
    buyer_id = body.get("buyer_id")
    product_id = body.get("product_id")
    quantity = body.get("quantity", 1)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (buyer_id, product_id, quantity, status) VALUES (%s, %s, %s, 'pending') RETURNING id",
        (buyer_id, product_id, quantity),
    )
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": order_id}


# VULN: idor — returns any order by id; never checks that it belongs to the
# authenticated caller, and there is no authentication check at all.
@router.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, buyer_id, product_id, quantity, status, created_at FROM orders WHERE id = %s", (order_id,)
    )
    r = cur.fetchone()
    cur.close()
    conn.close()
    if not r:
        return {"error": "not found"}
    return {"id": r[0], "buyer_id": r[1], "product_id": r[2], "quantity": r[3], "status": r[4], "created_at": str(r[5])}
