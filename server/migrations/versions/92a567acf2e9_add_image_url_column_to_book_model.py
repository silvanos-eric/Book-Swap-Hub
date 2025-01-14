"""add image_url column to book model

Revision ID: 92a567acf2e9
Revises: 1c25314e59ed
Create Date: 2024-10-21 21:27:34.443666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92a567acf2e9'
down_revision = '1c25314e59ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###
