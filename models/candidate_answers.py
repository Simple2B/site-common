from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import db


class CandidateAnswer(db.Model):
    __tablename__ = "candidate_answers"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("candidates.id"), nullable=False)
    answer_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("variant_answers.id"), nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True), default=datetime.now)

    answer = orm.relationship("VariantAnswer", viewonly=True)

    @hybrid_property
    def question(self):
        return self.answer.question

    @hybrid_property
    def is_right(self):
        return self.answer.answer_mark == self.question.correct_answer_mark

    def __repr__(self) -> str:
        return f"<{self.id}: at {self.created_at}, is right {self.is_right}>"