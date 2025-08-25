"""Add longitude and latitude columns for geotagging

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add longitude and latitude columns to mizu_sensor_hub table."""
    op.add_column('mizu_sensor_hub', sa.Column('longitude', sa.Float(), nullable=True))
    op.add_column('mizu_sensor_hub', sa.Column('latitude', sa.Float(), nullable=True))


def downgrade() -> None:
    """Remove longitude and latitude columns from mizu_sensor_hub table."""
    op.drop_column('mizu_sensor_hub', 'latitude')
    op.drop_column('mizu_sensor_hub', 'longitude')
