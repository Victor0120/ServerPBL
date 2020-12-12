"""empty message

Revision ID: 0f1727988770
Revises: 0c599e46711a
Create Date: 2020-12-12 18:59:49.090015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f1727988770'
down_revision = '0c599e46711a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('message', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('message_history')
    with op.batch_alter_table('course_material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filename', sa.String(length=150), nullable=True))
        batch_op.drop_column('data')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('course_material', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data', sa.BLOB(), nullable=True))
        batch_op.drop_column('filename')

    op.create_table('message_history',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('course_id', sa.INTEGER(), nullable=True),
    sa.Column('receiver_id', sa.INTEGER(), nullable=True),
    sa.Column('sender_id', sa.INTEGER(), nullable=True),
    sa.Column('created_on', sa.DATETIME(), nullable=False),
    sa.Column('message', sa.VARCHAR(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('message')
    # ### end Alembic commands ###