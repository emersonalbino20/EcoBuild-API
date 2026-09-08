from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.adapter_org import AdapterOrganization
from domain.use_cases.organization import (create_organization_case,
                                            get_organizations_case,
                                            remove_organization_case,
                                            update_organization_case)
from db.Session import get_db
from domain.organization import Organization
from schemas.organization import CreateField, UpdateField, OrganizationResponse
from utils.response_util import to_response

router = APIRouter(
    prefix="/organizations",
    tags=["organization"]
    )

@router.get("/", response_model=list[OrganizationResponse])
async def get_organizations(db: AsyncSession = Depends(get_db)) -> list[OrganizationResponse]:
    adapter = AdapterOrganization(db)
    result = await get_organizations_case(adapter)

    return [
      to_response(OrganizationResponse, organization)
      for organization in result
    ]

@router.post(
  "/",
  response_model=OrganizationResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_organization(
    organization: CreateField,
    db: AsyncSession = Depends(get_db)
) -> OrganizationResponse:
    adapter = AdapterOrganization(db)
    request = Organization(
        name=organization.name,
        location=organization.location
    )
    result = await create_organization_case(adapter, request)

    return to_response(OrganizationResponse, result)

@router.put("/{id}", response_model=OrganizationResponse)
async def update_organization(
    id: int,
    organization: UpdateField,
    db: AsyncSession = Depends(get_db)
) -> OrganizationResponse:
    adapter = AdapterOrganization(db)
    request = Organization(
        name=organization.name,
        location=organization.location
    )
    result = await update_organization_case(adapter, id, request)

    return to_response(OrganizationResponse, result)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(id: int, db: AsyncSession = Depends(get_db)) -> None:
    adapter = AdapterOrganization(db)
    await remove_organization_case(adapter, id)
