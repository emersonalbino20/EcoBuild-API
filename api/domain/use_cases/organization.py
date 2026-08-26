from domain.errors import NOT_FOUND
from domain.organization import Organization
from domain.ports import OrganizationRepository

async def get_organizations_case(
    org: OrganizationRepository,
) -> list[Organization]:

    return await org.get_organizations()

async def create_organization_case(
    org: OrganizationRepository,
    request: Organization
) -> Organization:

    assert request.user_id is not None, "User ID must be provided"
    is_user = await org.user_existing(request.user_id)

    if not is_user:
        raise NOT_FOUND(detail="User not found")

    return await org.create_organization(request)

async def update_organization_case(
    org: OrganizationRepository,
    id: int,
    request: Organization
) -> Organization | None:
  
    is_org = await org.organization_existing(id)
    if not is_org:
        raise NOT_FOUND(detail="Organization not found")

    return await org.update_organization(id, request)

async def remove_organization_case(
    org: OrganizationRepository,
    id: int
) -> None:
    is_org = await org.organization_existing(id)

    if not is_org:
        raise NOT_FOUND(detail="Organization not found")

    return await org.delete_organization(id)
