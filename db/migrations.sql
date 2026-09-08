-- migrations.sql
-- VULN: rls-disabled — Row Level Security is intentionally left OFF on every
-- table below. Combined with the service_role key being exposed client-side
-- (see /frontend/src/config/supabase.js and /backend/config.py), the anon
-- key AND the browser bundle can read/write every row in every table.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL, -- VULN: plaintext-password — no hashing/salt, ever
    role TEXT NOT NULL DEFAULT 'customer', -- 'admin' | 'customer'
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'pending', -- pending | paid | shipped
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    author_id INTEGER REFERENCES users(id),
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- VULN: rls-disabled — these are deliberately commented out. In a real app
-- every one of these tables should have RLS enabled with policies scoping
-- rows to the authenticated user.
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE products ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
