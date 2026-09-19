"""seed_catalog_materials_usd

Revision ID: e37cf01b9273
Revises: 9e012a85b302
Create Date: 2026-09-19 13:04:01.955662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e37cf01b9273'
down_revision: Union[str, Sequence[str], None] = '9e012a85b302'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
