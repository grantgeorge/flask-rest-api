"""get rid of ends_at

Revision ID: 61dc90daec64
Revises: e381a34cbad4
Create Date: 2020-01-03 14:00:41.358591

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '61dc90daec64'
down_revision = 'e381a34cbad4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_completions_ends_at', table_name='completions')
    op.drop_column('completions', 'ends_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('completions', sa.Column('ends_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.create_index('ix_completions_ends_at', 'completions', ['ends_at'], unique=False)
    # ### end Alembic commands ###
