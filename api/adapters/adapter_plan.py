from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.domain.ports import PlanRepository
from api.domain.plan import Plan
from api.models.plan import PlanModel
from api.models.organization import OrganizationModel

class AdapterPlan(PlanRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_plans(self, organization_id: int) -> list[Plan]:
        query = select(PlanModel).where(PlanModel.organization_id == organization_id)
        result = await self.db.execute(query)
        plans = result.scalars().all()

        return [
            Plan(
                plan.id,
                plan.organization_id,
                plan.storage_reference,
                plan.format,
                plan.size,
                plan.created_at
            )
            for plan in plans
        ]

    async def get_plan_by_id(self, id: int) -> Plan:
        query = select(PlanModel).where(PlanModel.id == id)
        result = await self.db.execute(query)
        plan = result.scalar_one_or_none()

        return Plan(
            plan.id,
            plan.organization_id,
            plan.storage_reference,
            plan.format,
            plan.size,
            plan.created_at
        )

    async def create_plan(self, request: Plan) -> Plan:
        db_plan = PlanModel(
            organization_id=request.organization_id,
            storage_reference=request.storage_reference,
            format=request.format,
            size=request.size,
        )
        self.db.add(db_plan)
        await self.db.commit()
        await self.db.refresh(db_plan)

        return Plan(
            db_plan.id,
            db_plan.organization_id,
            db_plan.storage_reference,
            db_plan.format,
            db_plan.size,
            db_plan.created_at
        )

    async def delete_plan(self, id: int) -> None:
        query = select(PlanModel).where(PlanModel.id == id)
        result = await self.db.execute(query)
        db_plan = result.scalar_one_or_none()

        await self.db.delete(db_plan)
        await self.db.commit()

    async def organization_existing(self, organization_id: int) -> bool:
        db_organization = await self.db.get(OrganizationModel, organization_id)
        if db_organization:
            return True
        return False

    async def plan_existing(self, id: int) -> bool:
        db_plan = await self.db.get(PlanModel, id)
        if db_plan:
            return True
        return False
