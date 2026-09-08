> ⚠️ **Esta es una aplicación de demostración deliberadamente vulnerable, solo para pruebas de seguridad (escaneo con Aikido). No maneja datos reales y NO debe considerarse segura ni usarse como base para producción.**

# Vulnerable Marketplace — Backend

API en Python + FastAPI (SQL crudo vía psycopg2, sin ORM) del mini-marketplace vulnerable
usado como banco de pruebas de Aikido Security (SAST, DAST, SCA, secret scanning).
Ver el detalle de fallos en [VULNERABILITIES.md](VULNERABILITIES.md).

Frontend: [github.com/rromom/aikido-demo-frontend](https://github.com/rromom/aikido-demo-frontend) (desplegado en GitHub Pages).

## Base de datos (Supabase)
1. En el **SQL Editor** de tu proyecto Supabase, ejecuta en orden:
   - [db/migrations.sql](db/migrations.sql) — esquema, con **RLS deshabilitado a propósito**
   - [db/seed.sql](db/seed.sql) — datos de prueba (incluye un payload de XSS almacenado)

## Desarrollo local
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
La API queda en `http://localhost:8000`. Las credenciales de Supabase/Postgres/JWT
están hardcodeadas en `config.py` (a propósito, ver VULNERABILITIES.md) — no hace
falta configurar variables de entorno.

## Despliegue (Render, free tier)
1. [render.com](https://render.com) → New → Web Service → conectar este repo.
2. Runtime: Python 3 · Build: `pip install -r requirements.txt` · Start:
   `uvicorn main:app --host 0.0.0.0 --port $PORT` · Instance: Free.
3. Sin variables de entorno: los secretos están hardcodeados a propósito en `config.py`.
4. El free tier de Render se duerme tras ~15 min sin tráfico; el primer request
   después tarda ~30-60s en responder — comportamiento esperado de la demo.

## Usuarios de prueba (ver `db/seed.sql`)
| Email | Password | Rol |
|---|---|---|
| admin@example.com | admin123 | admin |
| root@example.com | toor | admin |
| alice@example.com | alice123 | customer |
| bob@example.com | bobpass1 | customer |
| carol@example.com | carol123 | customer |
| dave@example.com | davepass1 | customer |
| erin@example.com | erin123 | customer |
| frank@example.com | frankpass1 | customer |
| grace@example.com | grace123 | customer |
| heidi@example.com | heidipass1 | customer |

## Qué NO hacer con este repo
- No lo despliegues contra un proyecto Supabase que use datos reales.
- No reemplaces los secretos falsos por credenciales reales de un sistema que te importe.
- No "arregles" las vulnerabilidades: son el propósito del repo (comentarios `# VULN:`
  marcan cada una — ver [VULNERABILITIES.md](VULNERABILITIES.md)).
