# Mapa de vulnerabilidades intencionales — backend

Contraparte frontend: [aikido-demo-frontend/VULNERABILITIES.md](https://github.com/rromom/aikido-demo-frontend/blob/main/VULNERABILITIES.md).

| # | Vulnerabilidad | Archivo:Línea | Categoría OWASP | Escaneo Aikido esperado |
|---|-----------------|----------------|------------------|--------------------------|
| 1 | Service role key de Supabase hardcodeada en el backend | [config.py:5](config.py#L5) | A02:2021 Cryptographic Failures (CWE-798) | Secrets |
| 2 | Cadena de conexión Postgres con usuario/contraseña en claro | [config.py:11](config.py#L11) | A02:2021 Cryptographic Failures (CWE-798) | Secrets |
| 3 | `JWT_SECRET` débil y fijo (`"secret123"`) | [config.py:15](config.py#L15) | A07:2021 Identification & Authentication Failures | Secrets / SAST |
| 4 | API key falsa de Stripe (`sk_live_...`) hardcodeada | [config.py:19](config.py#L19) | A02:2021 Cryptographic Failures (CWE-798) | Secrets |
| 5 | Uso de la cadena de conexión hardcodeada para conectar a Postgres | [db.py:6](db.py#L6) | A02:2021 Cryptographic Failures | SAST |
| 6 | RLS deshabilitado en todas las tablas de Supabase | [db/migrations.sql:2](db/migrations.sql#L2) y [línea 42](db/migrations.sql#L42) | A01:2021 Broken Access Control | IaC / Cloud config |
| 7 | Contraseñas almacenadas en texto plano (esquema) | [db/migrations.sql:10](db/migrations.sql#L10) | A02:2021 Cryptographic Failures | SAST |
| 8 | SQLi en registro de usuario (`INSERT` por f-string) | [routes_auth.py:17](routes_auth.py#L17) | A03:2021 Injection | SAST / DAST |
| 9 | SQLi en login (`SELECT ... WHERE email='{email}'`) — bypass de autenticación | [routes_auth.py:35](routes_auth.py#L35) | A03:2021 Injection | SAST / DAST |
| 10 | Password en texto plano comparada/almacenada en login | [routes_auth.py:13](routes_auth.py#L13) | A02:2021 Cryptographic Failures | SAST |
| 11 | Log de credenciales y token en stdout | [routes_auth.py:49](routes_auth.py#L49) | A09:2021 Security Logging & Monitoring Failures | SAST |
| 12 | SQLi en búsqueda de productos (`GET /products?q=`) | [routes_products.py:12](routes_products.py#L12) | A03:2021 Injection | SAST / DAST |
| 13 | Comentarios devueltos sin escapar (habilita XSS almacenado en el frontend) | [routes_products.py:46](routes_products.py#L46) | A03:2021 Injection | SAST |
| 14 | SQLi al insertar comentarios (`POST /products/{id}/comments`) | [routes_products.py:59](routes_products.py#L59) | A03:2021 Injection | SAST / DAST |
| 15 | IDOR en `GET /orders/{id}` (sin auth ni verificación de ownership) | [routes_orders.py:71](routes_orders.py#L71) | A01:2021 Broken Access Control | DAST / SAST |
| 15b | IDOR en `GET /orders?buyer_id=` (lista pedidos de cualquier comprador) | [routes_orders.py:10](routes_orders.py#L10) | A01:2021 Broken Access Control | DAST / SAST |
| 16 | IDOR en `GET /users/{id}` (expone password en claro) | [routes_users.py:8](routes_users.py#L8) | A01:2021 Broken Access Control | DAST / SAST |
| 17 | `GET /admin/users` sin autenticación/autorización | [routes_admin.py:8](routes_admin.py#L8) | A01:2021 Broken Access Control | DAST / SAST |
| 18 | `GET /admin/orders` sin auth + SQLi en filtro `status` | [routes_admin.py:22-23](routes_admin.py#L22) | A01:2021 / A03:2021 | DAST / SAST |
| 19 | SSRF en `GET /proxy?url=` (fetch server-side de URL arbitraria) | [routes_utils.py:13](routes_utils.py#L13) | A10:2021 SSRF | SAST / DAST |
| 20 | Path traversal en `GET /download?file=` | [routes_utils.py:22](routes_utils.py#L22) | A01:2021 Broken Access Control (CWE-22) | SAST / DAST |
| 21 | Deserialización insegura: `yaml.load(..., Loader=yaml.Loader)` | [routes_utils.py:30](routes_utils.py#L30) | A08:2021 Software & Data Integrity Failures | SAST |
| 22 | JWT sin expiración (`exp` ausente) | [auth.py:8](auth.py#L8) | A07:2021 Identification & Authentication Failures | SAST |
| 23 | Verificación de firma JWT deshabilitada (acepta tokens forjados) | [auth.py:15](auth.py#L15) | A07:2021 Identification & Authentication Failures | SAST |
| 24 | CORS permisivo (`allow_origins=["*"]` + `allow_credentials=True`) | [main.py:15](main.py#L15) | A05:2021 Security Misconfiguration | SAST / IaC |
| 25 | Debug mode activo en FastAPI | [main.py:11](main.py#L11) | A05:2021 Security Misconfiguration | SAST |
| 26 | Dependencias Python desactualizadas con CVEs conocidos | [requirements.txt:1](requirements.txt#L1) (requests 2.19.1, urllib3 1.23, PyYAML 5.1, Jinja2 2.10.1, PyJWT 1.7.1) | A06:2021 Vulnerable & Outdated Components | SCA |
| 27 | Payload de XSS almacenado en el seed (`<img onerror=...>`) | [db/seed.sql:64-67](db/seed.sql#L64) | A03:2021 Injection | DAST (post-seed) |

## Cómo re-generar esta lista
```bash
grep -rn "VULN:" . --include="*.py" --include="*.sql" --include="*.txt"
```
