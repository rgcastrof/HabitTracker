from typing import Type, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel, Session, select
import logging

logger = logging.getLogger(__name__)

class CRUDBase:
    """
    Classe base para operações de CRUD genéricas em SQLModel

    Permite criar, ler, atulizar e deletar registros de qualquer modelo SQLModel

    Attributes:
        model (Type[SQLModel]): O modelo SQLModel que será manipulado pelo CRUD
    """
    def __init__(self, model: Type[SQLModel]) -> None:
        """
        Inicializa o CRUD com o modelo fornecido

        Args:
            model (Type[SQLModel]): Modelo SQLModel para operações CRUD
        """
        self.model = model

    def create(self, obj: SQLModel, db: Session) -> SQLModel | None:
        """
        Cria um novo registro no banco de dados

        Args:
            obj (SQLModel): Instância do modelo com os dados a serem inseridos
            db (Session): Sessão SQLAlchemy ativa

        Returns:
            SQLModel | None: Objeto criado com ID atualizado ou None em caso de erro
        """
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
        """
        Busca um registro pelo seu ID
        
        Args:
            obj_id (int): ID do registro
            db (Session): Sessão SQLAlchemy ativa

        Returns:
            SQLModel | None: Objeto encontrado ou None em caso de erro
        """
        return db.get(self.model, obj_id)

    def get_all(self, offset: int, limit: int, db: Session) -> Sequence[SQLModel]:
        """
        Retorna todos os registros do modelo, com paginação

        Args:
            offset (int): Número de registros a pular
            limit (int): Número máximo de registros a retornar
            db (Session): Sessão SQLAlchemy ativa

        Returns:
            Sequence[SQLModel]: Lista de objetos encontrados
        """
        stmt = select(self.model).offset(offset).limit(limit)
        return db.exec(stmt).all()

    def update(self, obj_id: int, obj: SQLModel, db: Session) -> SQLModel | None:
        """
        Atualiza um registro existente pelo ID

        Args:
            obj_id (int): ID do registro a ser atualizado
            obj (SQLModel): Dados novos do modelo
            db (Session): Sessão SQLAlchemy ativa

        Returns:
            SQLModel | None: Objeto atualizado ou None em caso de erro
        """
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
        """
        Deleta um registro pelo ID
        
        Args:
            obj_id (int): ID do objeto a ser deletado
            db (Session): Sessão SQLAlchemy ativa

        Returns:
            SQLModel | None: Objeto deletado ou None em caso de erro
        """
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
