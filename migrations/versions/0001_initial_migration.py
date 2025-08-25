"""Initial migration for mizu_sensor_hub table

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the mizu_sensor_hub table."""
    op.create_table('mizu_sensor_hub',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.String(length=100), nullable=False),
        sa.Column('ambient_temperature', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Float(), nullable=True),
        sa.Column('soil_moisture', sa.Float(), nullable=True),
        sa.Column('soil_temperature', sa.Float(), nullable=True),
        sa.Column('wind_speed', sa.Float(), nullable=True),
        sa.Column('transmitted', sa.Boolean(), nullable=False, default=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index(op.f('ix_mizu_sensor_hub_device_id'), 'mizu_sensor_hub', ['device_id'], unique=False)
    op.create_index(op.f('ix_mizu_sensor_hub_timestamp'), 'mizu_sensor_hub', ['timestamp'], unique=False)


def downgrade() -> None:
    """Drop the mizu_sensor_hub table."""
    op.drop_index(op.f('ix_mizu_sensor_hub_timestamp'), table_name='mizu_sensor_hub')
    op.drop_index(op.f('ix_mizu_sensor_hub_device_id'), table_name='mizu_sensor_hub')
    op.drop_table('mizu_sensor_hub')
