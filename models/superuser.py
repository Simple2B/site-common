from typing import Self

import sqlalchemy as sa
from sqlalchemy import orm

# must have this import
from app.database import db, AppUser
from app.logger import log

from .base_user import BaseUser
from .utils import make_hash, hash_verify, generate_uuid, ModelMixin


class SuperUser(db.Model, BaseUser, AppUser, ModelMixin):
    __tablename__ = "superusers"

    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)

    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    reset_password_uid: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        default=generate_uuid,
    )

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, user_id, password):
        query = cls.select().where(
            (sa.func.lower(cls.username) == sa.func.lower(user_id))
            | (sa.func.lower(cls.email) == sa.func.lower(user_id))
        )
        user: Self = db.session.scalar(query)
        if not user:
            log(log.WARNING, "user:[%s] not found", user_id)

        if user is not None and hash_verify(password, user.password_hash):
            return user

    def reset_password(self):
        self.password_hash = ""
        self.reset_password_uid = generate_uuid()
        self.save()

    def __repr__(self):
        return f"<{self.id}: {self.email}>"