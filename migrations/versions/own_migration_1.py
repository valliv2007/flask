"""test migration_3

Revision ID: yyy
Revises: b00253a6bd87
Create Date: 2023-05-04 10:59:18.698731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'yyy'
down_revision = 'ca764488bdc3'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE actors SET is_active = False
        """
    ))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE actors SET is_active = NULL
        """
    ))
