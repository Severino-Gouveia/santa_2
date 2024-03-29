"""v.10

Revision ID: dcf2b2d71de0
Revises: 330fce865cbe
Create Date: 2024-01-29 13:17:49.709840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcf2b2d71de0'
down_revision = '330fce865cbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resposta', schema=None) as batch_op:
        batch_op.add_column(sa.Column('evento', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resposta', schema=None) as batch_op:
        batch_op.drop_column('evento')

    # ### end Alembic commands ###
