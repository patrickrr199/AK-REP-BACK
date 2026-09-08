# VULN: hardcoded-secrets — every credential below is committed to source
# control instead of being read from environment variables / a secrets
# manager. This file is intentionally NOT in .gitignore.

# VULN: secret-exposure — Supabase SERVICE_ROLE key (bypasses Row Level
# Security entirely, unlike the anon/publishable key).
SUPABASE_URL = "https://flkysfylxwlymiseprdp.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_M4uLIJHXqG3UZGTdsNh9Kw_Fz-_8aj9"
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_REPLACE_WITH_FAKE_SERVICE_ROLE_KEY_FOR_DEMO_1234567890abcdef"

# VULN: hardcoded-db-credentials — full Postgres connection string with
# user/password committed to git.
DATABASE_URL = "postgresql://postgres:SuperSecretPassw0rd!@db.flkysfylxwlymiseprdp.supabase.co:5432/postgres"

# VULN: weak-jwt-secret — short, guessable, reused everywhere, never rotated.
JWT_SECRET = "secret123"
JWT_ALGORITHM = "HS256"

# VULN: third-party-secret-leak — fake but realistically-shaped Stripe live
# secret key committed to a utils/config file.
STRIPE_SECRET_KEY = "sk_live_51H8xXXXXXXXXXXXXXXXXXXXXfakeDemoKeyXXXXXXXXXXXXXXXXXXXXXXXX"
