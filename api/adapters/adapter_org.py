from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.domain.ports import OrganizationRepository
from api.domain.organization import Organization
from api.models.organization import OrganizationModel
from api.models.user import UserModel

class AdapterOrganization(OrganizationRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_organizations(self) -> list[Organization]:
        query = select(OrganizationModel)
        result = await self.db.execute(query)
        organizations = result.scalars().all()

        return [
            Organization(
                org.id,
                org.user_id,
                org.name,
                org.location,
                org.created_at,
                org.updated_at
            )
            for org in organizations
        ]

    async def get_organization_by_id(self, id: int) -> Organization:
        query = select(OrganizationModel).where(OrganizationModel.id == id)
        result = await self.db.execute(query)
        organization = result.scalar_one_or_none()

        assert organization is not None
        
        return Organization(
            organization.id,
            organization.user_id,
            organization.name,
            organization.location,
            organization.created_at,
            organization.updated_at
        )

    async def create_organization(self, request: Organization) -> Organization:
        db_organization = OrganizationModel(
            user_id=request.user_id,
            name=request.name,
            location=request.location
        )
        self.db.add(db_organization)
        await self.db.commit()
        await self.db.refresh(db_organization)

        return Organization(
            db_organization.id,
            db_organization.user_id,
            db_organization.name,
            db_organization.location,
            db_organization.created_at,
            db_organization.updated_at
        )

    async def update_organization(self, id: int, request: Organization) -> Organization:
        query = select(OrganizationModel).where(OrganizationModel.id == id)
        result = await self.db.execute(query)
        db_organization = result.scalar_one_or_none()

        assert db_organization is not None
        if request.name is not None:
            db_organization.name = request.name
        if request.location is not None:
            db_organization.location = request.location

        await self.db.commit()
        await self.db.refresh(db_organization)

        return Organization(
            db_organization.id,
            db_organization.user_id,
            db_organization.name,
            db_organization.location,
            db_organization.created_at,
            db_organization.updated_at
        )

    async def delete_organization(self, id: int) -> None:
        query = select(OrganizationModel).where(OrganizationModel.id == id)
        result = await self.db.execute(query)
        db_org = result.scalar_one_or_none()
        
        await self.db.delete(db_org)
        await self.db.commit()

    async def user_existing(self, user_id: int) -> bool:
        db_user = await self.db.get(UserModel, user_id)
        if db_user:
            return True
        return False

    async def organization_existing(self, id: int) -> bool:
        db_organization = await self.db.get(OrganizationModel, id)
        if db_organization:
            return True
        return False

