from typing import Type, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, Session, select
import logging

logger = logging.getLogger(__name__)

class CRUDBase:
    def __init__(self, model: Type[SQLModel]) -> None:
        self.model = model

    def create(self, obj: SQLModel, db: Session) -> SQLModel | None:
        try:
            db_model = self.model(**obj.model_dump())
            db.add(db_model)
            db.commit()
            db.refresh(db_model)
            return db_model
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao criar entrada no banco: {e}")
            return None

    def get_by_id(self, obj_id: int, db: Session) -> SQLModel | None:
        return db.get(self.model, obj_id)

    def get_all(self, offset: int, limit: int, db: Session) -> Sequence[SQLModel]:
        stmt = select(self.model).offset(offset).limit(limit)
        return db.exec(stmt).all()

    def update(self, obj_id: int, obj: SQLModel, db: Session) -> SQLModel | None:
        db_obj = db.get(self.model, obj_id)

        if db_obj:
            for key, value in obj.model_dump(exclude_unset=True).items():
                setattr(db_obj, key, value)
            try:
                db.commit()
                db.refresh(db_obj)
                return db_obj
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Erro ao atualizar entrada no banco: {e}")
                return None
        else:
            logger.error(f"Objeto com id: {obj_id} não encontrado")
            return None


    def delete(self, obj_id: int, db: Session) -> SQLModel | None:
        db_obj = db.get(self.model, obj_id)

        if db_obj:
            try:
                db.delete(db_obj)
                db.commit()
                return db_obj
            except SQLAlchemyError as e:
                db.rollback()
                logger.error(f"Erro ao deletar entrada no banco: {e}")
                return None

        else:
            logger.error(f"Objeto com id: {obj_id} não encontrado")
            return None
