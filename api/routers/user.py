from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.adapter_user import AdapterUser
from domain.use_cases.user import (create_user_case,
                                    get_users_case,
                                    remove_user_case,
                                    update_user_case)
from db.Session import get_db
from domain.user import User
from schemas.user import CreateField, UpdateField, UserResponse
from utils.response_util import to_response
from utils.security import generate_pass_hash

router = APIRouter(
    prefix="/users",
    tags=["user"]
    )

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    adapter = AdapterUser(db)
    result = await get_users_case(adapter)

    return [
      to_response(UserResponse, user)
      for user in result
    ]

@router.post(
  "/",
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_user(user: CreateField, db: AsyncSession = Depends(get_db)) -> UserResponse:
    adapter = AdapterUser(db)
    request = User(
        name=user.name,
        email=user.email,
        password_hash=generate_pass_hash(user.password_hash)
    )
    result = await create_user_case(adapter, request)

    return to_response(UserResponse, result)

@router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: int,
    user: UpdateField,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    adapter = AdapterUser(db)
    request = User(
        name=user.name,
        email=user.email
    )
    result = await update_user_case(adapter, id, request)

    return to_response(UserResponse, result)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)) -> None:
    adapter = AdapterUser(db)
    await remove_user_case(adapter, id)
