"""empty message

Revision ID: eec6923e4837
Revises: 
Create Date: 2021-12-16 12:26:17.671439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eec6923e4837"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("uuid", sa.String(length=50), nullable=False),
        sa.Column("firstname", sa.String(length=50), nullable=True),
        sa.Column("lastname", sa.String(length=50), nullable=True),
        sa.Column("username", sa.String(length=50), nullable=True),
        sa.Column("password", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("dateofreg", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "posts",
        sa.Column("pid", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("puuid", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["puuid"],
            ["users.uuid"],
        ),
        sa.PrimaryKeyConstraint("pid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posts")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
