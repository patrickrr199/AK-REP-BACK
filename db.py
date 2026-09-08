import psycopg2

from config import DATABASE_URL


# VULN: hardcoded-db-credentials — connects using the plaintext connection
# string imported from config.py instead of an environment variable.
def get_connection():
    return psycopg2.connect(DATABASE_URL)
