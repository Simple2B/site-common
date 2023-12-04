from typing import Self, TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


# must have this import
from app.database import db

from .base_user import BaseUser


if TYPE_CHECKING:
    from .candidate_answers import CandidateAnswer


class Candidate(db.Model, BaseUser):
    __tablename__ = "candidates"

    image_url: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    git_hub_id: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    current_question_id: orm.Mapped[int | None] = orm.mapped_column(
        sa.Integer, nullable=True, default=None
    )
    quiz_score: orm.Mapped[float] = orm.mapped_column(sa.Float, default=0.0)

    answers: orm.Mapped[list["CandidateAnswer"]] = orm.relationship()

    @classmethod
    def authenticate(cls, db: orm.Session, git_hub_id: str) -> Self | None:
        user: Self | None = db.scalar(cls.select().where(cls.git_hub_id == git_hub_id))
        return user

    @property
    def count_of_answers(self) -> int:
        return len(self.answers)

    @hybrid_property
    def question_ids(self) -> list[int]:
        return [answer.question.id for answer in self.answers]

    def __repr__(self):
        return f"<{self.id}: {self.username}>"
