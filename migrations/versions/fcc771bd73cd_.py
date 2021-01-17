"""empty message

Revision ID: fcc771bd73cd
Revises: 6ecfa6145ff9
Create Date: 2021-01-17 07:56:16.681073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcc771bd73cd'
down_revision = '6ecfa6145ff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_question_answer', schema=None) as batch_op:
        batch_op.drop_column('doc_path')

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doc_path', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('doc_path')

    with op.batch_alter_table('course_question_answer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doc_path', sa.VARCHAR(length=1000), nullable=True))

    # ### end Alembic commands ###