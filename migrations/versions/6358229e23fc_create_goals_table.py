"""create goals table

Revision ID: 6358229e23fc
Revises: aa86e98dee81
Create Date: 2020-01-03 10:39:19.681057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6358229e23fc'
down_revision = 'aa86e98dee81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goals_timestamp'), 'goals', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_goals_timestamp'), table_name='goals')
    op.drop_table('goals')
    # ### end Alembic commands ###
