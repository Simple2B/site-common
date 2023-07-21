import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


# must have this import
from app.database import db

from .base_user import BaseUser


class Candidate(db.Model, BaseUser):
    __tablename__ = "candidates"

    image_url: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    git_hub_id: orm.Mapped[str] = orm.mapped_column(sa.String(32), nullable=False)

    current_question_id: orm.Mapped[int] = orm.mapped_column(nullable=True, default=None)
    quiz_score: orm.Mapped[float] = orm.mapped_column(default=0)

    _answer = orm.relationship("CandidateAnswer", viewonly=True, lazy="dynamic")

    @classmethod
    def authenticate(cls, db, git_hub_id: int):
        user = db.query(cls).filter_by(git_hub_id=git_hub_id).first()
        if user is not None:
            return user

    @hybrid_property
    def count_of_answers(self):
        return self._answer.count()

    @hybrid_property
    def question_ids(self):
        return [answer.question.id for answer in self._answer.all()]

    def __repr__(self):
        return f"<{self.id}: {self.username}>"