"""habit and completions

Revision ID: e381a34cbad4
Revises: 6358229e23fc
Create Date: 2020-01-03 13:45:31.966181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e381a34cbad4'
down_revision = '6358229e23fc'
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
    op.create_table('habits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('frequency', sa.Enum('daily', 'specified', 'per_period', 'repeating', name='habit_frequency'), nullable=True),
    sa.Column('duration_count', sa.Integer(), nullable=True),
    sa.Column('duration_type', sa.Enum('days', 'weeks', 'months', 'years', name='duration_type'), nullable=True),
    sa.Column('successful', sa.Boolean(), nullable=True),
    sa.Column('starts_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('ends_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('completions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=True),
    sa.Column('ends_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_completions_created_at'), 'completions', ['created_at'], unique=False)
    op.create_index(op.f('ix_completions_ends_at'), 'completions', ['ends_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_completions_ends_at'), table_name='completions')
    op.drop_index(op.f('ix_completions_created_at'), table_name='completions')
    op.drop_table('completions')
    op.drop_table('habits')
    op.drop_index(op.f('ix_goals_timestamp'), table_name='goals')
    op.drop_table('goals')
    # ### end Alembic commands ###
