from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import UserRepository
from domain.user import User
from models.user import UserModel

class AdapterUser(UserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_users(self) -> list[User]:
        query = select(UserModel)
        result = await self.db.execute(query)
        users = result.scalars().all()

        return [
            User(
                user.id,
                user.name,
                user.email,
                user.password_hash,
                user.created_at,
                user.updated_at
            )
            for user in users
        ]

    async def get_user_by_id(self, id: int) -> User:
        query = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        assert user is not None
        
        return User(
            user.id,
            user.name,
            user.email,
            user.password_hash,
            user.created_at,
            user.updated_at
        )

    async def create_user(self, request: User) -> User:
        db_user = UserModel(
            name=request.name,
            email=request.email,
            password_hash=request.password_hash
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return User(
            db_user.id,
            db_user.name,
            db_user.email,
            db_user.password_hash,
            db_user.created_at,
            db_user.updated_at
        )

    async def update_user(self, id: int, request: User) -> User:
        query = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()

        assert db_user is not None
        if request.name is not None:
            db_user.name = request.name
        if request.email is not None:
            db_user.email = request.email

        await self.db.commit()
        await self.db.refresh(db_user)

        return User(
            db_user.id,
            db_user.name,
            db_user.email,
            db_user.password_hash,
            db_user.created_at,
            db_user.updated_at
        )

    async def delete_user(self, id: int) -> None:
        db_user = self.db.get(UserModel, id)

        await self.db.delete(db_user)
        await self.db.commit()

    async def user_existing(self, id: int) -> bool:
        db_user = await self.db.get(UserModel, id)
        if db_user:
            return True
        return False

