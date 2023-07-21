import uuid
from passlib.context import CryptContext

from app.database import db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_verify(secret: str, hash: str) -> bool:
    return pwd_context.verify(secret, hash)


def make_hash(value_to_hash: str) -> str:
    return pwd_context.hash(value_to_hash)


def generate_uuid() -> str:
    return str(uuid.uuid4())


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
