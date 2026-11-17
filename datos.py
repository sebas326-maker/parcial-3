from sqlalchemy import create_engine, select, String, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session
)


# =====================================
# ORM 1 - CONFIGURAR LA CONEXION
# =====================================

# El engine administra la conexion con el archivo SQLite zapateria.db.
# Si el archivo no existe, SQLite lo crea al abrir la primera conexion.
engine = create_engine("sqlite:///zapateria.db")


# =====================================
# ORM 2 - CREAR LA CLASE BASE
# =====================================

class Base(DeclarativeBase):
    pass


# =====================================
# ORM 3 - CREAR EL MODELO ZAPATO
# =====================================

class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    modelo: Mapped[str] = mapped_column(String)
    talla: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column(Float)


# =====================================
# ORM 4 - CREAR LA TABLA
# =====================================

def inicializar_bd():
    # Crea en la base todas las tablas de los modelos que heredan de Base.
    # Si la tabla ya existe, no se modifica ni se borran sus datos.
    Base.metadata.create_all(engine)


# =====================================
# ORM 5 - REGISTRAR ZAPATO
# =====================================

def crear_zapato(modelo, talla, precio):
    try:
        with Session(engine) as session:
            zapato = Zapato(modelo=modelo, talla=talla, precio=precio)
            session.add(zapato)
            session.commit()
        return True
    except SQLAlchemyError:
        return False


# =====================================
# ORM 6 - LISTAR ZAPATOS
# =====================================

def listar_zapatos():
    with Session(engine) as session:
        return list(session.scalars(select(Zapato).order_by(Zapato.id)).all())


# =====================================
# ORM 7 - BUSCAR POR ID
# =====================================

def buscar_zapato(id_zapato):
    with Session(engine) as session:
        # get() devuelve el objeto o None si no existe.
        return session.get(Zapato, id_zapato)


# =====================================
# ORM 8 - ACTUALIZAR PRECIO
# =====================================

def actualizar_precio(id_zapato, nuevo_precio):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)
        if zapato is None:
            return False
        zapato.precio = nuevo_precio
        session.commit()
        return True


# =====================================
# ORM 9 - ELIMINAR ZAPATO
# =====================================

def eliminar_zapato(id_zapato):
    with Session(engine) as session:
        zapato = session.get(Zapato, id_zapato)
        if zapato is None:
            return False
        session.delete(zapato)
        session.commit()
        return True
