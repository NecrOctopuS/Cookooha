"""empty message

Revision ID: 248ce8519e5a
Revises: 
Create Date: 2020-06-02 20:55:14.659647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '248ce8519e5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredient_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('picture', sa.String(length=200), nullable=True),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('servings', sa.Integer(), nullable=True),
    sa.Column('kcal', sa.Integer(), nullable=True),
    sa.Column('instruction', sa.String(length=2000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('ingredient_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_group_id'], ['ingredient_groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_recipes',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('recipes_ingredients',
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('ingredient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes_ingredients')
    op.drop_table('users_recipes')
    op.drop_table('ingredients')
    op.drop_table('users')
    op.drop_table('recipes')
    op.drop_table('ingredient_groups')
    # ### end Alembic commands ###