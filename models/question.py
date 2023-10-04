from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import generate_uuid, ModelMixin

if TYPE_CHECKING:
    from .variant_answers import VariantAnswer


class Question(db.Model, ModelMixin):
    __tablename__ = "questions"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    text: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=False)
    correct_answer_mark: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)

    uid: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), nullable=False, default=generate_uuid
    )

    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    variants: orm.Mapped[list["VariantAnswer"]] = orm.relationship()

    @property
    def vacancies_ids(self) -> list[int]:
        return [vacancy.id for vacancy in self.variants]

    @property
    def correct_answer(self):
        for answer in self.variants:
            if answer.answer_mark == self.correct_answer_mark:
                return answer

    def __repr__(self) -> str:
        return f"<{self.id}: {self.text}>"
