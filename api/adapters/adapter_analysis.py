from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import AnalysisRepository
from domain.analysis import Analysis
from domain.material_list import MaterialList
from domain.material_item import MaterialItem
from models.analysis import AnalysisModel, MaterialListModel
from models.plan import PlanModel

class AdapterAnalysis(AnalysisRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_analyses(self, plan_id: int) -> list[Analysis]:
        query = (
            select(AnalysisModel)
            .options(
                selectinload(AnalysisModel.material_list).selectinload(
                    MaterialListModel.materials
                )
            )
            .where(AnalysisModel.plan_id == plan_id)
        )

        result = await self.db.execute(query)
        analyses_orm = result.scalars().all()

        return [
            Analysis(
                id=analysis.id,
                plan_id=analysis.plan_id,
                parent_analysis_id=analysis.parent_analysis_id,
                status=analysis.status,
                # Instancie MaterialListDomain explicitamente
                material_list=(
                    MaterialList(
                        id=analysis.material_list.id,
                        notes=analysis.material_list.notes,
                        materials=[
                            MaterialItem(
                                id=item.id,
                                material_list_id=item.material_list_id,
                                name=item.name,
                                quantity=item.quantity,
                                unit=item.unit,
                            )
                            for item in analysis.material_list.materials
                        ],
                    )
                    if analysis.material_list
                    else None
                ), # type: ignore
                created_at=analysis.created_at,
            )
            for analysis in analyses_orm
        ]

    
    async def get_analysis_by_id(self, id: UUID) -> Analysis | None:
        query = (
            select(AnalysisModel)
            .options(
                selectinload(AnalysisModel.material_list).selectinload(
                    MaterialListModel.materials
                )
            )
            .where(AnalysisModel.id == id)
        )

        # Use .scalars() antes de pedir o objeto ORM único
        result = await self.db.execute(query)
        analysis = result.scalars().first()

        if analysis is None:
            return None  # Retorna None conforme a assinatura da porta

        # Mapeamento seguro: com selectinload + .scalars(), os dados estão 100% em memória
        material_list_domain = None
        if analysis.material_list:
            material_list_domain = MaterialList(
                id=analysis.material_list.id,
                notes=analysis.material_list.notes,
                materials=[
                    MaterialItem(
                        id=item.id,
                        material_list_id=item.material_list_id,
                        name=item.name,
                        quantity=item.quantity,
                        unit=item.unit,
                    )
                    for item in analysis.material_list.materials
                ],
            )

        return Analysis(
            id=analysis.id,
            plan_id=analysis.plan_id,
            parent_analysis_id=analysis.parent_analysis_id,
            status=analysis.status,
            material_list=material_list_domain, # type: ignore
            created_at=analysis.created_at,
        )

    async def update_analysis(self, id: UUID, request: Analysis) -> None:
            query = select(AnalysisModel).where(AnalysisModel.id == id)
            result = await self.db.execute(query)
            db_analysis = result.scalar_one_or_none()
    
            assert db_analysis is not None
            db_analysis.status = request.status
            db_analysis.material_list_id = request.material_list_id

            await self.db.commit()
            await self.db.refresh(db_analysis)


    async def create_analysis(self, request: Analysis) -> Analysis:
        db_analysis = AnalysisModel(
            id=request.id,
            plan_id=request.plan_id,
            parent_analysis_id=request.parent_analysis_id,
        )
        self.db.add(db_analysis)
        await self.db.commit()
        await self.db.refresh(db_analysis)

        return  Analysis(
                        db_analysis.id,
                        db_analysis.plan_id,
                        db_analysis.parent_analysis_id,
                        db_analysis.status,
                        db_analysis.material_list, # type: ignore
                        db_analysis.material_list_id, # type: ignore
                        db_analysis.created_at
                    )

    async def plan_existing(self, plan_id: int) -> bool:
        db_plan = await self.db.get(PlanModel, plan_id)
        if db_plan:
            return True
        return False
