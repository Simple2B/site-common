from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm


from .utils import generate_uuid


class BaseUser:
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid, index=True)

    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), nullable=True, unique=True
    )
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), default="", unique=True
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.utcnow
    )
    is_verified: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
