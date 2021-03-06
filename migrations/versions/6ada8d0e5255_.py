"""empty message

Revision ID: 6ada8d0e5255
Revises:
Create Date: 2020-05-13 19:37:20.933116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6572aada3491'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cleanned_tweet',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('text', sa.Text(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cleanned_tweet')
    # ### end Alembic commands ###
