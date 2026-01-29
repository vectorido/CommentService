from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetAllUsersUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)
from src.domain.exceptions import EntityAlreadyExists, EntityNotFound, ValidationError
from src.presentation.api.dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_get_all_users_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
)
from src.presentation.schemas.user_schemas import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreateRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    try:
        user = await use_case.execute(email=request.email, name=request.name)
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except EntityAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    try:
        user = await use_case.execute(user_id=user_id)
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    limit: int = 100,
    offset: int = 0,
    use_case: GetAllUsersUseCase = Depends(get_get_all_users_use_case),
):
    users = await use_case.execute(limit=limit, offset=offset)
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
):
    try:
        user = await use_case.execute(user_id=user_id, email=request.email, name=request.name)
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
):
    try:
        await use_case.execute(user_id=user_id)
    except EntityNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

