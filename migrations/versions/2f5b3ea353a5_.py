"""empty message

Revision ID: 2f5b3ea353a5
Revises: 97e2275a9d34
Create Date: 2020-12-04 23:03:52.148343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f5b3ea353a5'
down_revision = '97e2275a9d34'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('message_history', 'message')


def downgrade():
    op.rename_table('message', 'message_history')
