"""empty message

Revision ID: bedff43f6e05
Revises: da4127ee6ee4
Create Date: 2023-09-15 16:25:48.702227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bedff43f6e05'
down_revision = 'da4127ee6ee4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint('epoch_id', type_='foreignkey')
        batch_op.drop_column('epoch_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('epoch_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('epoch_id', 'epoch', ['epoch_id'], ['id'])

    # ### end Alembic commands ###