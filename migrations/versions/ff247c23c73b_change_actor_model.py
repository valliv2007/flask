"""change_actor_model

Revision ID: ff247c23c73b
Revises: 63849ff66949
Create Date: 2023-03-27 13:07:41.197187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff247c23c73b'
down_revision = '63849ff66949'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.create_unique_constraint('Name', ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###
