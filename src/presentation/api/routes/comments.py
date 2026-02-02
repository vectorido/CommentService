from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query

from src.application.use_cases.comment_use_cases import (
    CreateCommentUseCase,
    GetCommentsUseCase,
    UpdateCommentUseCase,
)
from src.domain.exceptions import (
    CommentNotFound,
    CommentValidationError,
    EntityNotFound,
)
from src.presentation.schemas.comment_schemas import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentOutSchema,
)
from src.presentation.api.dependencies import (
    get_create_comment_use_case,
    get_get_comments_use_case,
    get_update_comment_use_case,
)

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentOutSchema)
async def create_comment(
    payload: CommentCreateSchema,
    use_case: CreateCommentUseCase = Depends(get_create_comment_use_case),
):
    try:
        return await use_case.execute(
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            author_id=payload.author_id,
            text=payload.text,
        )
    except CommentValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CommentOutSchema])
async def get_comments(
    entity_type: str = Query(...),
    entity_id: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    sort: str = Query("desc", pattern="^(asc|desc)$"),
    use_case: GetCommentsUseCase = Depends(get_get_comments_use_case),
):
    try:
        return await use_case.execute(
            entity_type=entity_type,
            entity_id=entity_id,
            page=page,
            limit=limit,
            sort=sort,
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/", response_model=CommentOutSchema)
async def update_comment(
    payload: CommentUpdateSchema,
    use_case: UpdateCommentUseCase = Depends(get_update_comment_use_case),
):
    try:
        return await use_case.execute(
            comment_id=payload.comment_id,
            entity_type=payload.entity_type,
            entity_id=payload.entity_id,
            new_text=payload.new_text,
        )
    except (CommentNotFound, CommentValidationError, EntityNotFound) as e:
        raise HTTPException(status_code=400, detail=str(e))
