#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "luigelo@ldvloper.com"

from typing import Annotated
from urllib.parse import quote

from fastapi import File, Query, Response, UploadFile, status
from fastapi.routing import APIRouter

from src.module.infrastructure.serializers.documents.document_schemas import (
    DocumentList,
    DocumentPublic,
    DocumentTextPublic,
)
from src.routers.dependencies import CurrentUser, DocumentServiceDep


class Document:
    """
    Class proxy Document.
    """

    def __init__(self):
        self.router = APIRouter()
        self.set_customized_router()  # Add routes to the router

    @staticmethod
    def get_router():
        document = Document()
        return document.router

    def set_customized_router(self):
        """
        Customized router for Document.
        """

        @self.router.post(
            "",
            response_model=DocumentPublic,
            status_code=status.HTTP_202_ACCEPTED,
        )
        async def upload_document(
            current_user: CurrentUser,
            service: DocumentServiceDep,
            file: Annotated[UploadFile, File()],
        ):
            """
            Upload a document (PDF or UTF-8 text) and schedule its processing.

            The type is detected from the content, not from the file name.
            Poll `GET /documents/{id}` until `status` is `completed` or `failed`.

            Raises:
            - `413`: If the file is too large.
            - `415`: If the file type is not supported.
            """
            return await service.upload(current_user.id, file.filename, file.file)

        @self.router.get("", response_model=DocumentList)
        async def list_documents(
            current_user: CurrentUser,
            service: DocumentServiceDep,
            limit: Annotated[int, Query(ge=1, le=100)] = 20,
            offset: Annotated[int, Query(ge=0)] = 0,
        ):
            """
            List the documents of the authenticated user, newest first.
            """
            items = await service.list_documents(current_user.id, limit, offset)
            return DocumentList(
                items=[DocumentPublic.model_validate(d) for d in items],
                limit=limit,
                offset=offset,
            )

        @self.router.get("/{document_id}", response_model=DocumentPublic)
        async def get_document(
            document_id: str, current_user: CurrentUser, service: DocumentServiceDep
        ):
            """
            Get a document and its processing status.
            """
            return await service.get_document(current_user.id, document_id)

        @self.router.get(
            "/{document_id}/content",
            response_class=Response,
            responses={200: {"content": {"application/pdf": {}, "text/plain": {}}}},
        )
        async def download_document(
            document_id: str, current_user: CurrentUser, service: DocumentServiceDep
        ):
            """
            Download the original file.
            """
            document, content = await service.get_content(current_user.id, document_id)
            return Response(
                content=content,
                media_type=document.file_type.media_type,
                headers={
                    "Content-Disposition": _content_disposition(document.filename),
                    "X-Content-Type-Options": "nosniff",
                },
            )

        @self.router.get("/{document_id}/text", response_model=DocumentTextPublic)
        async def get_document_text(
            document_id: str, current_user: CurrentUser, service: DocumentServiceDep
        ):
            """
            Get the text extracted from a document, one entry per page.

            Raises:
            - `409`: If the document has not been processed yet.
            """
            text = await service.get_text(current_user.id, document_id)
            return DocumentTextPublic(
                document_id=text.document_id,
                page_count=len(text.pages),
                char_count=text.char_count,
                pages=text.pages,
            )

        @self.router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_document(
            document_id: str, current_user: CurrentUser, service: DocumentServiceDep
        ):
            """
            Delete a document, its file and its extracted text.
            """
            await service.delete_document(current_user.id, document_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)


def _content_disposition(filename: str) -> str:
    # ASCII fallback plus the RFC 5987 encoded name for non ASCII characters
    ascii_name = (
        filename.encode("ascii", "ignore").decode().replace('"', "") or "document"
    )
    return f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{quote(filename)}"
