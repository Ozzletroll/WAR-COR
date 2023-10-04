"""empty message

Revision ID: a29ebc70697f
Revises: 1628976579fa
Create Date: 2023-10-04 14:34:26.010700

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'a29ebc70697f'
down_revision = '1628976579fa'
branch_labels = None
depends_on = None


def upgrade():

    """Migration function to replace "-" with "/" in date fields"""

    # Update Event model
    op.execute(text("UPDATE event SET date = REPLACE(date, '-', '/')"))

    # Update Epoch model
    op.execute(text("UPDATE epoch SET start_date = REPLACE(start_date, '-', '/')"))
    op.execute(text("UPDATE epoch SET end_date = REPLACE(end_date, '-', '/')"))


def downgrade():
    pass
