"""empty message

Revision ID: 468efe9575f6
Revises: cd9f54db8230
Create Date: 2023-09-25 15:55:08.008570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '468efe9575f6'
down_revision = 'cd9f54db8230'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('following_event_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_following_event', 'event', ['following_event_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint('fk_following_event', type_='foreignkey')
        batch_op.drop_column('following_event_id')

    # ### end Alembic commands ###
