"""test migration_3

Revision ID: fff
Revises: d076891e0f59
Create Date: 2023-05-04 10:59:18.698731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fff'
down_revision = 'd076891e0f59'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE films SET is_released = TRUE WHERE release_date <= CURRENT_TIMESTAMP
        """
    ))
    conn.execute(sa.text(
        """
        UPDATE films SET is_released = FALSE WHERE release_date > CURRENT_TIMESTAMP
        """
    ))



def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text(
        """
        UPDATE films SET is_released = NULL
        """
    ))
