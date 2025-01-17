from typing import Generic, Type, TypeVar, Union

from sqlalchemy.orm import Session

from src.database.session import Base

ModelType = TypeVar("ModelType", bound=Base)


class CrudBase(Generic[ModelType]):
    def __init__(self, Model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.Model = Model

    def get(self, db: Session, id: int) -> Union[ModelType, None]:
        return db.query(self.Model).filter(self.Model.id == id).first()

    def create(self, db: Session, db_obj: ModelType) -> ModelType:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_many(self, db: Session, db_objs: list[ModelType]) -> list[ModelType]:
        db.add_all(db_objs)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs

    def update(self, db: Session, db_obj: ModelType) -> ModelType:
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> None:
        obj = db.query(self.Model).get(id)
        db.delete(obj)
        db.commit()
