"""Initial migration.

Revision ID: 1611acc656bd
Revises: 
Create Date: 2023-10-02 08:26:06.163104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1611acc656bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('new')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('new', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
