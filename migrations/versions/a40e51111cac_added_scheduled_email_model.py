"""Added Scheduled_Email model

Revision ID: a40e51111cac
Revises: 4c65e8dcda30
Create Date: 2024-02-11 20:28:13.244834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a40e51111cac'
down_revision = '4c65e8dcda30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scheduled__email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['email_id'], ['email.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scheduled__email')
    # ### end Alembic commands ###
