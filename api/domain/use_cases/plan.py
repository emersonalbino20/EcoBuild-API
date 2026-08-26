from domain.errors import NOT_FOUND
from domain.plan import Plan
from domain.ports import PlanRepository

async def get_plans_case(
    plan_repo: PlanRepository,
    organization_id: int
) -> list[Plan]:

    return await plan_repo.get_plans(organization_id)

async def get_plan_by_id_case(
    plan_repo: PlanRepository,
    id: int
) -> Plan:
    is_plan = await plan_repo.plan_existing(id)

    if not is_plan:
        raise NOT_FOUND(detail="Plan not found")

    return await plan_repo.get_plan_by_id(id)

async def create_plan_case(
    plan_repo: PlanRepository,
    request: Plan
) -> Plan:

    is_organization = await plan_repo.organization_existing(request.organization_id)

    if not is_organization:
        raise NOT_FOUND(detail="Organization not found")

    return await plan_repo.create_plan(request)



async def remove_plan_case(
    plan_repo: PlanRepository,
    id: int
) -> None:
    is_plan = await plan_repo.plan_existing(id)

    if not is_plan:
        raise NOT_FOUND(detail="Plan not found")

    return await plan_repo.delete_plan(id)
