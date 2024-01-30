"""img

Revision ID: 816e569471d4
Revises: ad4456f28950
Create Date: 2024-01-28 10:26:30.301746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '816e569471d4'
down_revision = 'ad4456f28950'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carousel_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_filename', sa.String(length=100), nullable=False),
    sa.Column('caption', sa.String(length=200), nullable=True),
    sa.Column('link_text', sa.String(length=100), nullable=True),
    sa.Column('link_url', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('carousel_item')
    # ### end Alembic commands ###
