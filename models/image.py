import sqlalchemy as sa
from sqlalchemy import orm


class Image:
    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    url: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)
    origin_file_name: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=False
    )
