from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import AnalysisRepository
from domain.analysis import Analysis
from models.analysis import AnalysisModel
from models.plan import PlanModel

class AdapterAnalysis(AnalysisRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_analyses(self, plan_id: int) -> list[Analysis]:
        query = select(AnalysisModel).where(AnalysisModel.plan_id == plan_id)
        result = await self.db.execute(query)
        analyses = result.scalars().all()

        return [
            Analysis(
                analysis.id,
                analysis.plan_id,
                analysis.parent_analysis_id or 0,
                analysis.version,
                int(analysis.estimated_cost or 0),
                int(analysis.waste_percentage or 0),
                int(analysis.co2_saved or 0),
                analysis.status,
                analysis.created_at
            )
            for analysis in analyses or []
        ]

    async def get_analysis_by_id(self, id: int) -> Analysis:
        query = select(AnalysisModel).where(AnalysisModel.id == id)
        result = await self.db.execute(query)
        analysis = result.scalar_one_or_none()

        assert analysis is not None

        return Analysis(
                        analysis.id,
                        analysis.plan_id,
                        analysis.parent_analysis_id or 0,
                        analysis.version,
                        int(analysis.estimated_cost or 0),
                        int(analysis.waste_percentage or 0),
                        int(analysis.co2_saved or 0),
                        analysis.status,
                        analysis.created_at
                    )

    async def create_analysis(self, request: Analysis) -> Analysis:
        db_analysis = AnalysisModel(
            plan_id=request.plan_id,
            parent_analysis_id=request.parent_analysis_id,
            version=request.version,
        )
        self.db.add(db_analysis)
        await self.db.commit()
        await self.db.refresh(db_analysis)

        return  Analysis(
                        db_analysis.id,
                        db_analysis.plan_id,
                        db_analysis.parent_analysis_id or 0,
                        db_analysis.version,
                        int(db_analysis.estimated_cost or 0),
                        int(db_analysis.waste_percentage or 0),
                        int(db_analysis.co2_saved or 0),
                        db_analysis.status,
                        db_analysis.created_at
                    )

    async def plan_existing(self, plan_id: int) -> bool:
        db_plan = await self.db.get(PlanModel, plan_id)
        if db_plan:
            return True
        return False
