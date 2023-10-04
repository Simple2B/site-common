from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db


if TYPE_CHECKING:
    from .question import Question


class VariantAnswer(db.Model):
    __tablename__ = "variant_answers"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    question_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("questions.id"), nullable=False
    )
    text: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)
    answer_mark: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)

    question: orm.Mapped["Question"] = orm.relationship(back_populates="variants")

    def __repr__(self) -> str:
        return f"<{self.id}: {self.text}>"
