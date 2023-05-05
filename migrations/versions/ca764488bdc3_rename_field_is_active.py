"""rename field is_active

Revision ID: ca764488bdc3
Revises: xxx
Create Date: 2023-05-04 11:29:58.393599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca764488bdc3'
down_revision = 'xxx'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.drop_column('is_action')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_action', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
