import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import generate_uuid, ModelMixin


class Device(db.Model, ModelMixin):
    __tablename__ = "devices"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uid: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), nullable=False, default=generate_uuid
    )
    token = orm.mapped_column(sa.String(512), nullable=False)

    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Device token: {self.token}>"
