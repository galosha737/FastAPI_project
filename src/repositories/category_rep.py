from sqlalchemy.orm import Session
from ..infrastructure.sqlite.models import Category
from ..schems.category_s import CategoryUpdateAndCreate
from typing import List, Optional


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self, skip: int = 0, limit: int = 10) -> List[Category]:
        category_list = self.session.query(Category).offset(skip).limit(limit).all()
        return category_list # type: ignore

    def get(self, category_id: int) -> Optional[Category]:
        return self.session.get(Category, category_id)

    def create(self, data: CategoryUpdateAndCreate) -> Category:
        category = Category(**data.model_dump()) # type: ignore
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def update(self, category_id: int, data: CategoryUpdateAndCreate) -> Optional[Category]:
        category = self.get(category_id)
        if not category:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        self.session.commit()
        self.session.refresh(category)
        return category

    def delete(self, category_id: int) -> Optional[Category]:
        category = self.get(category_id)
        if not category:
            return None
        self.session.delete(category)
        self.session.commit()
        return category