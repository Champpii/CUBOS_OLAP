from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DimFecha(Base):
    __tablename__ = 'DIM_FECHA'
    fecha_key = Column(Integer, primary_key=True, autoincrement=True)
    fecha_completa = Column(Date, nullable=False, unique=True)
    dia = Column(Integer, nullable=False)
    dia_semana = Column(String(20), nullable=False)
    semana = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    trimestre = Column(Integer, nullable=False)
    año = Column(Integer, nullable=False)
    indicador_fin_semana = Column(Boolean, nullable=False)
    indicador_feriado = Column(Boolean, nullable=False)

class DimCategoria(Base):
    __tablename__ = 'DIM_CATEGORIA'
    categoria_key = Column(Integer, primary_key=True, autoincrement=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion = Column(String)
    categoria_padre = Column(Integer, ForeignKey('DIM_CATEGORIA.categoria_key'), nullable=True)
    subcategorias = relationship("DimCategoria", remote_side=[categoria_key])

    def to_dict(self):
        return {
            "categoria_key": self.categoria_key,
            "nombre_categoria": self.nombre_categoria,
            "descripcion": self.descripcion,
            "categoria_padre": self.categoria_padre
        }

class DimMarca(Base):
    __tablename__ = 'DIM_MARCA'
    marca_key = Column(Integer, primary_key=True, autoincrement=True)
    nombre_marca = Column(String(100), nullable=False, unique=True)

class DimModelo(Base):
    __tablename__ = 'DIM_MODELO'
    modelo_key = Column(Integer, primary_key=True, autoincrement=True)
    nombre_modelo = Column(String(100), nullable=False)
    año_lanzamiento = Column(Integer, nullable=False)
    marca_key = Column(Integer, ForeignKey('DIM_MARCA.marca_key'), nullable=False)
    marca = relationship("DimMarca")

class DimProducto(Base):
    __tablename__ = 'DIM_PRODUCTO'
    producto_key = Column(Integer, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(100), nullable=False)
    descripcion = Column(String)
    modelo_key = Column(Integer, ForeignKey('DIM_MODELO.modelo_key'), nullable=False)
    año_fabricacion = Column(Integer, nullable=False)
    color = Column(String(30))
    precio_lista = Column(DECIMAL(10, 2), nullable=False)
    categoria_key = Column(Integer, ForeignKey('DIM_CATEGORIA.categoria_key'), nullable=False)
    modelo = relationship("DimModelo")
    categoria = relationship("DimCategoria")

class FactVentas(Base):
    __tablename__ = 'FACT_VENTAS'
    venta_key = Column(Integer, primary_key=True, autoincrement=True)
    fecha_key = Column(Integer, ForeignKey('DIM_FECHA.fecha_key'), nullable=False)
    producto_key = Column(Integer, ForeignKey('DIM_PRODUCTO.producto_key'), nullable=False)
    cantidad_vendida = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    descuento_aplicado = Column(DECIMAL(10, 2), default=0.00)
    margen_ganancia = Column(DECIMAL(10, 2), nullable=False)
