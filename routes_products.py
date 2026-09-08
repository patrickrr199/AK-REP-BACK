from fastapi import APIRouter, Request

from db import get_connection

router = APIRouter()


@router.get("/products")
def list_products(q: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    # VULN: sql-injection — search term concatenated straight into a LIKE clause,
    # e.g. q = "' UNION SELECT email,password,... FROM users -- " leaks user data.
    query = f"SELECT id, title, description, price, stock, seller_id FROM products WHERE title LIKE '%{q}%'"
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "title": r[1], "description": r[2], "price": float(r[3]), "stock": r[4], "seller_id": r[5]}
        for r in rows
    ]


@router.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, price, stock, seller_id FROM products WHERE id = %s", (product_id,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    if not r:
        return {"error": "not found"}
    return {"id": r[0], "title": r[1], "description": r[2], "price": float(r[3]), "stock": r[4], "seller_id": r[5]}


@router.get("/products/{product_id}/comments")
def get_comments(product_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, author_id, body, created_at FROM comments WHERE product_id = %s", (product_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # VULN: no-output-encoding — comment body is returned raw; the frontend
    # renders it with v-html, enabling the stored XSS payload from the seed data.
    return [{"id": r[0], "author_id": r[1], "body": r[2], "created_at": str(r[3])} for r in rows]


@router.post("/products/{product_id}/comments")
async def add_comment(product_id: int, request: Request):
    body = await request.json()
    author_id = body.get("author_id")
    text = body.get("body")

    conn = get_connection()
    cur = conn.cursor()
    # VULN: sql-injection — comment body concatenated directly into the INSERT,
    # which also doubles as a stored-XSS injection point since it is later
    # rendered unsanitized on the frontend.
    query = f"INSERT INTO comments (product_id, author_id, body) VALUES ({product_id}, {author_id}, '{text}') RETURNING id"
    cur.execute(query)
    comment_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": comment_id}
