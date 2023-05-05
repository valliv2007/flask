"""add contact model

Revision ID: 830e401c95d8
Revises: yyy
Create Date: 2023-05-04 11:40:35.002825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '830e401c95d8'
down_revision = 'yyy'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=False),
    sa.Column('address', sa.String(length=150), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contacts')
    # ### end Alembic commands ###
