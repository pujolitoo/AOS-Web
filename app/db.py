import os
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from app.models.product import Producto

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()


class ProductORM(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


engine = None
SessionLocal = None


def init_db():
    global engine, SessionLocal
    if not DATABASE_URL:
        return
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)


def list_products_db() -> List[Producto]:
    if not SessionLocal:
        return []
    session = SessionLocal()
    try:
        rows = session.query(ProductORM).all()
        return [Producto(id=r.id, nombre=r.nombre, precio=r.precio, stock=r.stock) for r in rows]
    finally:
        session.close()


def get_product_db(id: int) -> Optional[Producto]:
    if not SessionLocal:
        return None
    session = SessionLocal()
    try:
        r = session.query(ProductORM).filter(ProductORM.id == id).first()
        if not r:
            return None
        return Producto(id=r.id, nombre=r.nombre, precio=r.precio, stock=r.stock)
    finally:
        session.close()


def create_product_db(producto: Producto):
    if not SessionLocal:
        raise RuntimeError("DB not configured")
    session = SessionLocal()
    try:
        row = ProductORM(id=producto.id, nombre=producto.nombre, precio=producto.precio, stock=producto.stock)
        session.add(row)
        session.commit()
        return producto
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def update_product_db(id: int, producto: Producto):
    if not SessionLocal:
        raise RuntimeError("DB not configured")
    session = SessionLocal()
    try:
        row = session.query(ProductORM).filter(ProductORM.id == id).first()
        if not row:
            return None
        row.nombre = producto.nombre
        row.precio = producto.precio
        row.stock = producto.stock
        session.commit()
        return producto
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def delete_product_db(id: int) -> bool:
    if not SessionLocal:
        raise RuntimeError("DB not configured")
    session = SessionLocal()
    try:
        row = session.query(ProductORM).filter(ProductORM.id == id).first()
        if not row:
            return False
        session.delete(row)
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def patch_product_db(id: int, cambios) -> Optional[Producto]:
    if not SessionLocal:
        raise RuntimeError("DB not configured")
    session = SessionLocal()
    try:
        row = session.query(ProductORM).filter(ProductORM.id == id).first()
        if not row:
            return None
        if getattr(cambios, "nombre", None) is not None:
            row.nombre = cambios.nombre
        if getattr(cambios, "precio", None) is not None:
            row.precio = cambios.precio
        if getattr(cambios, "stock", None) is not None:
            row.stock = cambios.stock
        session.commit()
        return Producto(id=row.id, nombre=row.nombre, precio=row.precio, stock=row.stock)
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()
