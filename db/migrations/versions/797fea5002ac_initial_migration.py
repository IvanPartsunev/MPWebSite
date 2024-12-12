"""Initial migration

Revision ID: 797fea5002ac
Revises: 
Create Date: 2024-12-12 23:25:38.672702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '797fea5002ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('is_email_confirmed', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('is_phone_confirmed', sa.Boolean(), server_default='FALSE', nullable=False),
    sa.Column('updated_by', sa.String(length=36), nullable=True),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('roles',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_by', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_roles',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('role_id', sa.String(length=36), nullable=False),
    sa.Column('added_by', sa.String(length=36), nullable=True),
    sa.Column('added_on', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['added_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('roles')
    op.drop_table('users')
    # ### end Alembic commands ###
