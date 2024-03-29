"""v.12

Revision ID: 80abc08e8d8d
Revises: dcf2b2d71de0
Create Date: 2024-01-29 17:34:06.980325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80abc08e8d8d'
down_revision = 'dcf2b2d71de0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resposta', schema=None) as batch_op:
        batch_op.drop_column('de_manha')
        batch_op.drop_column('a_tarde')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resposta', schema=None) as batch_op:
        batch_op.add_column(sa.Column('a_tarde', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('de_manha', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
