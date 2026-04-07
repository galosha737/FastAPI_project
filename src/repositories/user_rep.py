from sqlalchemy.orm import Session
from ..infrastructure.sqlite.models import User
from ..schems.user_s import UserCreate, UserUpdate
from typing import List, Optional


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self, skip: int = 0, limit: int = 10) -> List[User]:
        user_list = self.session.query(User).offset(skip).limit(limit).all()
        return user_list # type: ignore

    def get(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def create(self, data: UserCreate) -> User:
        # mode="json" для SecretStr
        user = User(**data.model_dump(mode="json"))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        self.session.delete(user)
        self.session.commit()
        return user

