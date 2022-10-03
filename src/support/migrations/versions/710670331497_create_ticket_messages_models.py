"""Create ticket & messages models

Revision ID: 710670331497
Revises: a9e5ec83e114
Create Date: 2022-10-03 16:38:57.448714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '710670331497'
down_revision = 'a9e5ec83e114'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('message_text', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('tickets')
    # ### end Alembic commands ###