from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel

from src.application.use_cases.comment_use_cases import (
    CreateCommentUseCase,
    GetCommentsUseCase,
    UpdateCommentUseCase
)
from src.domain.exceptions import CommentNotFound, CommentValidationError
from src.domain.exceptions import EntityNotFound


class CommentCreateSchema(BaseModel):
    entity_type: str
    entity_id: str
    author_id: str
    text: str


class CommentUpdateSchema(BaseModel):
    comment_id: str
    entity_type: str
    entity_id: str
    new_text: str


class CommentOutSchema(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    author_id: str
    text: str
    created_at: str
    updated_at: str


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentOutSchema)
async def create_comment(payload: CommentCreateSchema):
    use_case = CreateCommentUseCase()
    try:
        comment = await use_case.execute(
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            author_id=payload.author_id,
            text=payload.text
        )
        return comment
    except CommentValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CommentOutSchema])
async def get_comments(
        entity_type: str = Query(...),
        entity_id: str = Query(...),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        sort: str = Query("desc", regex="^(asc|desc)$")
):
    use_case = GetCommentsUseCase()
    try:
        comments = await use_case.execute(
            entity_type=entity_type,
            entity_id=entity_id,
            page=page,
            limit=limit,
            sort=sort
        )
        return comments
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/", response_model=CommentOutSchema)
async def update_comment(payload: CommentUpdateSchema):
    use_case = UpdateCommentUseCase()
    try:
        comment = await use_case.execute(
            comment_id=payload.comment_id,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            new_text=payload.new_text
        )
        return comment
    except (CommentNotFound, CommentValidationError, EntityNotFound) as e:
        raise HTTPException(status_code=400, detail=str(e))
