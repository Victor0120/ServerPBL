"""empty message

Revision ID: 964b6f5bbd6e
Revises: da030bb2b1af
Create Date: 2021-01-04 11:50:23.132710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '964b6f5bbd6e'
down_revision = 'da030bb2b1af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('qa_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('model_id', sa.String(length=100), nullable=False),
    sa.Column('model_type', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('qa_model')
    # ### end Alembic commands ###
