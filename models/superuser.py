from typing import Self

import sqlalchemy as sa
from sqlalchemy import orm

# must have this import
from app.database import db

from .base_user import BaseUser
from .utils import make_hash, hash_verify


class SuperUser(db.Model, BaseUser):
    __tablename__ = "superusers"

    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, db, user_id: str, password: str) -> Self:
        user = (
            db.query(cls)
            .filter(
                sa.or_(
                    sa.func.lower(cls.username) == sa.func.lower(user_id),
                    sa.func.lower(cls.email) == sa.func.lower(user_id),
                )
            )
            .first()
        )
        if user is not None and hash_verify(password, user.password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.email}>"