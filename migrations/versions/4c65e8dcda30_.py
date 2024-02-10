"""empty message

Revision ID: 4c65e8dcda30
Revises: 
Create Date: 2024-02-10 23:48:23.738672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c65e8dcda30'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('email',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('email_subject', sa.String(length=250), nullable=True),
        sa.Column('email_content', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('fullname', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('email')
    op.drop_table('user')
