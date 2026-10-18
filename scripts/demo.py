#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

"""
End to end demo against a running API: register, log in, upload a document, wait
for the worker to process it and print the extracted text.

    docker compose run --rm demo
    API_URL=http://localhost:8000 python scripts/demo.py [path/to/file.pdf]

Uses only the standard library, so it runs anywhere Python does.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

API_URL = os.environ.get("API_URL", "http://localhost:8000").rstrip("/")
# Address to open in a browser, when the script runs inside the Compose network
PUBLIC_URL = os.environ.get("PUBLIC_URL", API_URL).rstrip("/")
EMAIL = os.environ.get("DEMO_EMAIL", "demo@example.com")
PASSWORD = os.environ.get("DEMO_PASSWORD", "demo-password-123")
SAMPLE = Path(__file__).resolve().parent.parent / "samples" / "sample.pdf"


def request(method, path, body=None, headers=None, form=None, file=None):
    headers = dict(headers or {})
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    elif form is not None:
        data = urllib.parse.urlencode(form).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif file is not None:
        boundary = uuid.uuid4().hex
        name, content = file
        data = (
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{name}"\r\n'
                "Content-Type: application/octet-stream\r\n\r\n"
            ).encode()
            + content
            + f"\r\n--{boundary}--\r\n".encode()
        )
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    req = urllib.request.Request(  # noqa: S310 - API_URL is http(s)
        API_URL + path, data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:  # noqa: S310
            return response.status, json.loads(response.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def step(message):
    print(f"\n==> {message}")


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else SAMPLE

    step(f"Registering {EMAIL}")
    status, body = request("POST", "/users", {"email": EMAIL, "password": PASSWORD})
    if status == 409:
        print("already registered")
    elif status != 201:
        sys.exit(f"Registration failed: {status} {body}")
    else:
        print("created")

    step("Logging in")
    status, body = request(
        "POST", "/oauth2/token", form={"username": EMAIL, "password": PASSWORD}
    )
    if status != 200:
        sys.exit(f"Login failed: {status} {body}")
    auth = {"Authorization": f"Bearer {body['access_token']}"}
    print(f"token expires in {body['expires_in']}s")

    step(f"Uploading {path.name}")
    status, document = request(
        "POST", "/documents", headers=auth, file=(path.name, path.read_bytes())
    )
    if status != 202:
        sys.exit(f"Upload failed: {status} {document}")
    print(f"document {document['id']} is {document['status']}")

    step("Waiting for the worker")
    for _ in range(60):
        status, document = request("GET", f"/documents/{document['id']}", headers=auth)
        if document["status"] in ("completed", "failed"):
            break
        time.sleep(1)
    print(json.dumps(document, indent=2))
    if document["status"] != "completed":
        sys.exit("Processing did not complete")

    step("Extracted text")
    status, text = request("GET", f"/documents/{document['id']}/text", headers=auth)
    for number, page in enumerate(text["pages"], start=1):
        print(f"--- page {number} ---")
        print(page.strip())

    print(f"\nDone. Explore the API at {PUBLIC_URL}/docs")


if __name__ == "__main__":
    main()
