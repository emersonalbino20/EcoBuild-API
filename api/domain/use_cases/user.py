from domain.errors import NOT_FOUND
from domain.user import User
from domain.ports import UserRepository


async def get_users_case(
    user: UserRepository,
) -> list[User]:

    return await user.get_users()

async def create_user_case(
    user: UserRepository,
    request: User
) -> User:

    return await user.create_user(request)

async def update_user_case(
    user: UserRepository,
    id: int,
    request: User
) -> User | None:
    is_user = await user.user_existing(id)

    if not is_user:
        raise NOT_FOUND(detail="User not found")

    return await user.update_user(id, request)

async def remove_user_case(
    user: UserRepository,
    id: int
) -> None:
    is_user = await user.user_existing(id)

    if not is_user:
        raise NOT_FOUND(detail="User not found")

    return await user.delete_user(id)
