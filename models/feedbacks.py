# flake8: noqa F821

import sqlalchemy as sa
from sqlalchemy import orm


# must have this import
from app.database import db
from .enum import Languages
from .utils import generate_uuid


class FeedBack(db.Model):
    __tablename__ = "feedbacks"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36), default=generate_uuid, index=True
    )
    client_name: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)
    project_name: orm.Mapped[str | None] = orm.mapped_column(
        sa.String(128), nullable=False
    )

    comment: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=False)
    language: orm.Mapped[str] = orm.mapped_column(
        sa.String(16), nullable=False, default=Languages.ENGLISH.value
    )

    def __repr__(self):
        return f"<{self.id}: {self.client_name}>"
