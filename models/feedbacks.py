# flake8: noqa F821
from random import randint
from urllib.parse import urljoin
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
    link: orm.Mapped[str | None] = orm.mapped_column(sa.String(512), default=None)

    comment: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=False)
    language: orm.Mapped[str] = orm.mapped_column(
        sa.String(16), nullable=False, default=Languages.ENGLISH.value
    )

    @property
    def img_url(self):
        return urljoin("https://static.simple2b.net", f"/feedbacks/{randint(1, 14)}.svg")

    def __repr__(self):
        return f"<{self.id}: {self.client_name}>"
