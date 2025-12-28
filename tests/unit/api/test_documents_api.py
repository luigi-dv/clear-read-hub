#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"


def _upload(client, headers, content: bytes, filename: str = "paper.pdf"):
    return client.post(
        "/documents", headers=headers, files={"file": (filename, content)}
    )


def test_upload_requires_authentication(client, pdf_factory):
    assert _upload(client, {}, pdf_factory(["x"])).status_code == 401


def test_upload_process_and_read_text(client, auth_headers, pdf_factory):
    content = pdf_factory(["Readability matters", "Second page"])
    response = _upload(client, auth_headers, content)
    assert response.status_code == 202
    document_id = response.json()["id"]

    # The inline queue processes the document during the upload request
    document = client.get(f"/documents/{document_id}", headers=auth_headers).json()
    assert document["status"] == "completed"
    assert document["page_count"] == 2
    assert document["file_type"] == "pdf"

    text = client.get(f"/documents/{document_id}/text", headers=auth_headers).json()
    assert text["page_count"] == 2
    assert "Readability matters" in text["pages"][0]


def test_download_original_content(client, auth_headers):
    document_id = _upload(client, auth_headers, b"hello", "notesé.txt").json()["id"]
    response = client.get(f"/documents/{document_id}/content", headers=auth_headers)
    assert response.status_code == 200
    assert response.content == b"hello"
    assert response.headers["content-type"].startswith("text/plain")
    assert response.headers["x-content-type-options"] == "nosniff"
    disposition = response.headers["content-disposition"]
    assert 'filename="notes.txt"' in disposition
    assert "filename*=UTF-8''notes%C3%A9.txt" in disposition


def test_corrupt_pdf_is_reported_as_failed(client, auth_headers):
    document = _upload(client, auth_headers, b"%PDF-1.4 broken").json()
    stored = client.get(f"/documents/{document['id']}", headers=auth_headers).json()
    assert stored["status"] == "failed"
    assert stored["error"]
    text = client.get(f"/documents/{document['id']}/text", headers=auth_headers)
    assert text.status_code == 409


def test_unsupported_type(client, auth_headers):
    response = _upload(client, auth_headers, b"PK\x03\x04zip", "a.docx")
    assert response.status_code == 415


def test_too_large(client, auth_headers, settings):
    content = b"a" * (settings.MAX_UPLOAD_BYTES + 1)
    assert _upload(client, auth_headers, content, "a.txt").status_code == 413


def test_list_documents(client, auth_headers, register):
    for i in range(3):
        _upload(client, auth_headers, f"text {i}".encode(), f"{i}.txt")
    other_headers = register("other@example.com")
    _upload(client, other_headers, b"other", "other.txt")

    page = client.get("/documents?limit=2", headers=auth_headers).json()
    assert len(page["items"]) == 2
    assert page["limit"] == 2
    rest = client.get("/documents?limit=2&offset=2", headers=auth_headers).json()
    assert len(rest["items"]) == 1
    names = {d["filename"] for d in page["items"] + rest["items"]}
    assert names == {"0.txt", "1.txt", "2.txt"}


def test_list_limit_is_bounded(client, auth_headers):
    assert client.get("/documents?limit=1000", headers=auth_headers).status_code == 422


def test_other_users_cannot_access_documents(client, auth_headers, register):
    document_id = _upload(client, auth_headers, b"private").json()["id"]
    intruder = register("intruder@example.com")
    for path in ("", "/content", "/text"):
        response = client.get(f"/documents/{document_id}{path}", headers=intruder)
        assert response.status_code == 404
    assert (
        client.delete(f"/documents/{document_id}", headers=intruder).status_code == 404
    )
    assert (
        client.get(f"/documents/{document_id}", headers=auth_headers).status_code == 200
    )


def test_delete_document(client, auth_headers, storage):
    document_id = _upload(client, auth_headers, b"text").json()["id"]
    assert (
        client.delete(f"/documents/{document_id}", headers=auth_headers).status_code
        == 204
    )
    assert (
        client.get(f"/documents/{document_id}", headers=auth_headers).status_code == 404
    )
    assert storage.files == {}
