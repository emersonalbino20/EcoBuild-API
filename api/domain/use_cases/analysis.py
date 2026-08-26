from domain.errors import NOT_FOUND
from domain.analysis import Analysis
from domain.ports import AnalysisRepository

async def get_analyses_case(
    analysis_repo: AnalysisRepository,
    plan_id: int
) -> list[Analysis]:

    return await analysis_repo.get_analyses(plan_id)

async def get_analysis_by_id_case(
    analysis_repo: AnalysisRepository,
    id: int
) -> Analysis:
    is_plan = await analysis_repo.plan_existing(id)

    if not is_plan:
        raise NOT_FOUND(detail="Plan not found")

    return await analysis_repo.get_analysis_by_id(id)

async def create_analysis_case(
    analysis_repo: AnalysisRepository,
    request: Analysis
) -> Analysis:

    is_plan = await analysis_repo.plan_existing(request.plan_id)

    if not is_plan:
        raise NOT_FOUND(detail="Plan not found")

    return await analysis_repo.create_analysis(request)
