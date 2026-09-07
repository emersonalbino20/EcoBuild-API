from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from api.adapters.adapter_plan import AdapterPlan
from api.domain.use_cases.plan import (create_plan_case,
                                        get_plans_case,
                                        get_plan_by_id_case,
                                        remove_plan_case
                                        )
from api.db.Session import get_db
from api.adapters.adapter_storage import DocumentStorageAdapter
from api.domain.plan import Plan
from api.schemas.plan import PlanResponse
from api.utils.response_util import to_response

router = APIRouter(
    prefix="/plans",
    tags=["plan"]
    )

@router.get("/{organization_id}", response_model=list[PlanResponse])
async def get_plans(org_id: int, db: AsyncSession = Depends(get_db)) -> list[PlanResponse]:
    adapter = AdapterPlan(db)
    result = await get_plans_case(adapter, org_id)

    return [
      to_response(PlanResponse, plan)
      for plan in result
    ]

@router.get("/org/{plan_id}", response_model=PlanResponse)
async def get_plan(plan_id: int, db: AsyncSession = Depends(get_db)) -> PlanResponse:
    adapter = AdapterPlan(db)
    result = await get_plan_by_id_case(adapter, plan_id)

    return to_response(PlanResponse, result)

UPLOAD_DIR = Path("api/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_storage_adapter() -> DocumentStorageAdapter:
    return DocumentStorageAdapter(upload_dir="api/uploads", max_size_mb=5)

@router.post(
  "/{organization_id}",
  response_model=PlanResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_organization(
    org_id: int,
    file: UploadFile = File(...),
    storage_adapter: DocumentStorageAdapter = Depends(get_storage_adapter),
    db: AsyncSession = Depends(get_db)
) -> PlanResponse:
    adapter = AdapterPlan(db)

    file_metadata = await storage_adapter.save_document(file)

    request = Plan(
        organization_id=org_id,
        storage_reference=str(file_metadata.get("location")),
        format=str(file_metadata.get("content_type")),
        size=int(file_metadata.get("size") or 0)    # type: ignore
    )
    result = await create_plan_case(adapter, request)

    return to_response(PlanResponse, result)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(id: int, db: AsyncSession = Depends(get_db)) -> None:
    adapter = AdapterPlan(db)
    await remove_plan_case(adapter, id)