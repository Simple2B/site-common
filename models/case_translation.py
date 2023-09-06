# flake8: noqa F821
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


# must have this import
from app.database import db
from .case_image import CaseImage

from .enum import Language


class CaseTranslation(db.Model):
    __tablename__ = "cases_translations"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    case_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("cases.id"), nullable=False
    )
    title: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), nullable=False, unique=True
    )
    sub_title: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=False)
    role: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    language: orm.Mapped[Language] = orm.mapped_column(
        sa.Enum(Language), nullable=False, default=Language.GERMAN
    )
    case: orm.Mapped[CaseImage] = orm.relationship(
        "Case", viewonly=True, backref="translations"
    )

    def __repr__(self):
        return f"<{self.id}: {self.title}, {self.language}>"
