import os

import requests
import yaml
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "files")


# VULN: ssrf — fetches any attacker-supplied URL server-side (including
# internal/metadata endpoints like http://169.254.169.254/...) and echoes the
# response back to the caller.
@router.get("/proxy")
def proxy(url: str):
    resp = requests.get(url)
    return {"status": resp.status_code, "body": resp.text[:2000]}


# VULN: path-traversal — filename comes straight from the query string with
# no sanitization, e.g. file=../../../../etc/passwd.
@router.get("/download")
def download(file: str):
    path = os.path.join(UPLOAD_DIR, file)
    return FileResponse(path)


# VULN: insecure-deserialization — yaml.load with the full Loader (not
# SafeLoader) allows arbitrary Python object construction / code execution
# from a crafted YAML file.
@router.get("/config")
def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "seed_config.yaml")
    with open(config_path) as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data
