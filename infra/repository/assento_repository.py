from infra.configs.connection import DBConnectionHandler
from infra.entities.Assento import Assento
from infra.entities.Aviao import Aviao
from typing import Type

class AssentoRepository:
    def select(self) -> Type[DBConnectionHandler]:
        with DBConnectionHandler() as db:
            data = db.session\
                .query(Assento, Aviao)\
                .join(Assento, Aviao.id == Assento.id_aviao)\
                .with_entities(Assento.assento_id, Assento.ocupado, Aviao.nome)\
                .all()
            return data

    def insert(self, assento_id: str, aviao: Type[Aviao], ocupado: bool) -> None:
        with DBConnectionHandler() as db:
            data_insert = Assento(assento_id = assento_id, 
                    id_aviao = aviao.id,
                    ocupado = ocupado)
            db.session.add(data_insert)
            db.session.commit()

    def delete(self, id: int) -> None:
        with DBConnectionHandler() as db:
            data = db.session.query(Assento).filter(Assento.id == id).delete()
            db.session.commit()

    def update_ocupado(self, id: int, ocupado: bool) -> None:
        with DBConnectionHandler() as db:
            data = db.session.query(Assento).filter(Assento.id == id).update(ocupado = ocupado)
            db.session.commit()
