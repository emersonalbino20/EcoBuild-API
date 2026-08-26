from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.adapter_analysis import AdapterAnalysis
from domain.use_cases.analysis import (create_analysis_case,
                                        get_analyses_case)

from db.Session import get_db
from domain.analysis import Analysis, AnalysisStatus
from schemas.analysis import CreateField, AnalysisResponse
from utils.response_util import to_response

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

@router.post(
  "/",
  response_model=AnalysisResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_analysis(
    analysis: CreateField,
    db: AsyncSession = Depends(get_db)
) -> AnalysisResponse:
    adapter = AdapterAnalysis(db)
    request = Analysis(
        plan_id=analysis.plan_id,
        parent_analysis_id=analysis.parent_analysis_id,
        version=1,
        estimated_cost=0,
        waste_percentage=0,
        co2_saved=0,
        status= AnalysisStatus.PROCESSING    
    )
    result = await create_analysis_case(adapter, request)

    return to_response(AnalysisResponse, result)
