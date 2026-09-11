from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from api.adapters.adapter_analysis import AdapterAnalysis
from api.adapters.adapter_material_list import AdapterMaterialList
from api.adapters.adapter_material_item import AdapterMaterialItem
from api.domain.use_cases.analysis import (create_analysis_case, update_analysis_case,
                                        get_analyses_case)
from api.domain.use_cases.material_list import create_material_list_case
from api.domain.use_cases.material_item import create_material_item_case
from api.db.Session import get_db
from api.domain.analysis import Analysis, AnalysisStatus
from api.domain.material_item import MaterialItem
from api.domain.material_list import MaterialList
from api.material_estimation.agent_estimation import get_estimation
from api.material_estimation.schemas.estimate_data import MaterialList as AgentResponse
from api.routers.plan import get_plan
from api.schemas.analysis import CreateField, AnalysisResponse
from api.utils.response_util import to_response

router = APIRouter(
    prefix="/analyses",
    tags=["analysis"]
    )

@router.get("/{plan_id}", response_model=list[AnalysisResponse])
async def get_analyses(plan_id: int, db: AsyncSession = Depends(get_db)) -> list[AnalysisResponse]:
    adapter = AdapterAnalysis(db)
    result = await get_analyses_case(adapter, plan_id)

    return [
      to_response(AnalysisResponse, plan)
      for plan in result
    ]

async def generate_material(
        request: Analysis, 
        storage_reference: str,
        format: str,
        db: AsyncSession = Depends(get_db)):
    try:
        agent: AgentResponse = await get_estimation(storage_reference, format)

        list_id: UUID = uuid4()

        adapter_list = AdapterMaterialList(db)
        request_m_list = MaterialList(
            id=list_id,
            notes=agent.notes,
        )
        await create_material_list_case(adapter_list, request_m_list)

        items_to_create = [
            MaterialItem(
                id=uuid4(),
                material_list_id=list_id,
                name=item.name,
                quantity=item.quantity,
                unit=item.unit,
            )
            for item in agent.materials
        ]

        adapter_item = AdapterMaterialItem(db)

        await create_material_item_case(adapter_item, items_to_create)

        adapter_analysis = AdapterAnalysis(db)

        await update_analysis_case(adapter_analysis, request.id, Analysis(
            id=request.id,
            material_list_id=list_id,
            status=AnalysisStatus.READY))
        
    except Exception as e:
        await db.rollback()

        adapter_analysis = AdapterAnalysis(db)

        await update_analysis_case(adapter_analysis, request.id, Analysis(
                    id=request.id,
                    status=AnalysisStatus.FAILED))
        print(f"Error generating material: {e}")


@router.post(
    "/",
    response_model=AnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_analysis(
    analysis: CreateField,
    tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    adapter = AdapterAnalysis(db)
    unique: UUID = uuid4()

    request = Analysis(
        id=unique,
        plan_id=analysis.plan_id,
        parent_analysis_id=unique,
    )

    result = await create_analysis_case(adapter, request)

    plan = await get_plan(analysis.plan_id, db)

    tasks.add_task(generate_material, request, plan.storage_reference, plan.format, db)

    return to_response(AnalysisResponse, result)
