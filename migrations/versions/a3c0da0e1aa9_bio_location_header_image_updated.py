"""bio, location, header image updated

Revision ID: a3c0da0e1aa9
Revises: 6e1db5433cbb
Create Date: 2018-03-21 13:44:13.574774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3c0da0e1aa9'
down_revision = '6e1db5433cbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###
