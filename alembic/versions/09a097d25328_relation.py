"""relation

Revision ID: 09a097d25328
Revises: 58fcf9ab912e
Create Date: 2024-09-30 18:29:41.605774

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "09a097d25328"
down_revision: Union[str, None] = "58fcf9ab912e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("items", sa.Column("price", sa.Float(), nullable=True))
    op.add_column("items", sa.Column("quantity", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("items", "quantity")
    op.drop_column("items", "price")
    # ### end Alembic commands ###
