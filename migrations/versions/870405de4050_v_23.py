"""v.23

Revision ID: 870405de4050
Revises: 8bafbf57dfa6
Create Date: 2024-02-10 06:52:18.079090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '870405de4050'
down_revision = '8bafbf57dfa6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mensagem_email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('assunto', sa.String(length=100), nullable=False),
    sa.Column('mensagem', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mensagem_email')
    # ### end Alembic commands ###
