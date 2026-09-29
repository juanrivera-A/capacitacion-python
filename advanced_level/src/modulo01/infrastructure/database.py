import os
from pathlib import Path

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Si hay una variable de entorno DB_DIR la usa (ej: en Docker /app/data),
# si no, usará una carpeta 'data' relativa al directorio donde vive este archivo.
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DB_DIR", BASE_DIR / "data"))

# Crear el directorio si no existe
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Ruta absoluta al archivo SQLite
DB_PATH = DATA_DIR / "orders.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

sessionmaker_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    status = Column(String, nullable=False)


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
