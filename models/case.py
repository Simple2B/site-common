# flake8: noqa F821
from typing import List

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


# must have this import
from app.database import db
from .case_stacks import case_stacks
from .stack import Stack
from .case_screenshot import CaseScreenshot
from .case_image import CaseImage, EnumCaseImageType
from .enum import Language


class Case(db.Model):
    __tablename__ = "cases"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(
        sa.String(32), nullable=False, unique=True
    )

    sub_title: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=False)

    is_active: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=True
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False
    )
    project_link: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    is_main: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False
    )

    role: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    _stacks: orm.Mapped[List["Stack"]] = orm.relationship(
        "Stack",
        secondary=case_stacks,
        backref="_cases",
        viewonly=True,
    )

    _screenshots: orm.Mapped[List["CaseScreenshot"]] = orm.relationship(
        "CaseScreenshot", viewonly=True
    )

    case_images: orm.Mapped[CaseImage] = orm.relationship(
        "CaseImage", viewonly=True, lazy="dynamic"
    )

    @property
    def germany_translation(self):
        translations = [
            translation
            for translation in self.translations
            if translation.language == Language.GERMAN
        ]
        if translations:
            return translations[0]
        return self

    @property
    def stacks_names(self) -> list[str]:
        return [stack.name for stack in self._stacks]

    @property
    def stacks(self) -> list["Stack"]:
        return self._stacks

    @property
    def screenshots(self) -> list["CaseScreenshot"]:
        return self._screenshots

    @property
    def screenshots_urls(self) -> list[str]:
        return [screenshot.url for screenshot in self._screenshots]

    @hybrid_property
    def main_image_url(self) -> str:
        image: CaseImage | None = (
            self.case_images.filter_by(
                type_of_image=EnumCaseImageType.case_main_image, is_deleted=False
            )
            .order_by(CaseImage.id.desc())
            .limit(1)
            .first()
        )

        if image:
            return image.url
        return ""

    @hybrid_property
    def preview_image_url(self) -> str:

        image: CaseImage | None = (
            self.case_images.filter_by(
                type_of_image=EnumCaseImageType.case_preview_image, is_deleted=False
            )
            .order_by(CaseImage.id.desc())
            .limit(1)
            .first()
        )

        if image:
            return image.url
        return ""

    @hybrid_property
    def slug_name(self) -> str:
        return self.title.strip().replace(" ", "-").replace("_", "-").lower()

    def as_dict(self):
        case_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        case_dict["_stacks"] = [stack.as_dict() for stack in self._stacks]

        return case_dict

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<{self.id}: {self.title}>"
