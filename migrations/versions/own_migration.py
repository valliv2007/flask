"""test migration

Revision ID: xxx
Revises: b00253a6bd87
Create Date: 2023-05-04 10:59:18.698731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'xxx'
down_revision = 'b00253a6bd87'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE films SET test = 100 WHERE title like '%Deathly%'
        """
    ))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE films SET test = NULL WHERE title like '%Deathly%'
        """
    ))
