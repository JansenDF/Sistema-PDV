from src.db.base import Base
from src.db.connectdb import engine

# IMPORTAR todos os modelos antes de criar
from src.models import models

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Tabelas criadas com sucesso!")
