from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

class Models:
    def __init__(self, db):
        self.db = db

        class DimFecha(db.Model):
            __tablename__ = 'DIM_FECHA'
            __table_args__ = {'extend_existing': True}

            fecha_key = Column(Integer, primary_key=True, autoincrement=True)
            fecha_completa = Column(Date, nullable=False, unique=True)
            dia = Column(Integer, nullable=False)
            dia_semana = Column(String(20), nullable=False)
            semana = Column(Integer, nullable=False)
            mes = Column(Integer, nullable=False)
            trimestre = Column(Integer, nullable=False)
            ano = Column(Integer, nullable=False)
            indicador_fin_semana = Column(Boolean, nullable=False)
            indicador_feriado = Column(Boolean, nullable=False)

            def to_dict(self):
                return {
                    "fecha_key": self.fecha_key,
                    "fecha_completa": self.fecha_completa.isoformat(),
                    "dia": self.dia,
                    "dia_semana": self.dia_semana,
                    "semana": self.semana,
                    "mes": self.mes,
                    "trimestre": self.trimestre,
                    "año": self.ano,
                    "indicador_fin_semana": self.indicador_fin_semana,
                    "indicador_feriado": self.indicador_feriado
                }

        self.DimFecha = DimFecha

        class DimCategoria(db.Model):
            __tablename__ = 'DIM_CATEGORIA'
            __table_args__ = {'extend_existing': True}

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

        self.DimCategoria = DimCategoria

        class DimMarca(db.Model):
            __tablename__ = 'DIM_MARCA'
            __table_args__ = {'extend_existing': True}

            marca_key = Column(Integer, primary_key=True, autoincrement=True)
            nombre_marca = Column(String(100), nullable=False, unique=True)

            def to_dict(self):
                return {
                    "marca_key": self.marca_key,
                    "nombre_marca": self.nombre_marca
                }

        self.DimMarca = DimMarca

        class DimModelo(db.Model):
            __tablename__ = 'DIM_MODELO'
            __table_args__ = {'extend_existing': True}

            modelo_key = Column(Integer, primary_key=True, autoincrement=True)
            nombre_modelo = Column(String(100), nullable=False)
            ano_lanzamiento = Column(Integer, nullable=False)
            marca_key = Column(Integer, ForeignKey('DIM_MARCA.marca_key'), nullable=False)
            marca = relationship("DimMarca")

            def to_dict(self):
                return {
                    "modelo_key": self.modelo_key,
                    "nombre_modelo": self.nombre_modelo,
                    "año_lanzamiento": self.ano_lanzamiento,
                    "marca_key": self.marca_key
                }

        self.DimModelo = DimModelo

        class DimProducto(db.Model):
            __tablename__ = 'DIM_PRODUCTO'
            __table_args__ = (
                UniqueConstraint('nombre_producto', 'modelo_key', name='uq_producto_modelo'),
                {'extend_existing': True}
            )

            producto_key = Column(Integer, primary_key=True, autoincrement=True)
            nombre_producto = Column(String(100), nullable=False)
            descripcion = Column(String)
            modelo_key = Column(Integer, ForeignKey('DIM_MODELO.modelo_key'), nullable=False)
            ano_fabricacion = Column(Integer, nullable=False)
            color = Column(String(30))
            precio_lista = Column(DECIMAL(10, 2), nullable=False)
            categoria_key = Column(Integer, ForeignKey('DIM_CATEGORIA.categoria_key'), nullable=False)
            modelo = relationship("DimModelo")
            categoria = relationship("DimCategoria")

            def to_dict(self):
                return {
                    "producto_key": self.producto_key,
                    "nombre_producto": self.nombre_producto,
                    "descripcion": self.descripcion,
                    "modelo_key": self.modelo_key,
                    "año_fabricacion": self.ano_fabricacion,
                    "color": self.color,
                    "precio_lista": str(self.precio_lista),
                    "categoria_key": self.categoria_key
                }

        self.DimProducto = DimProducto

        class FactVentas(db.Model):
            __tablename__ = 'FACT_VENTAS'
            __table_args__ = (
                CheckConstraint('cantidad_vendida > 0', name='ck_cantidad_vendida_positive'),
                CheckConstraint('precio_unitario >= 0', name='ck_precio_unitario_positive'),
                CheckConstraint('margen_ganancia >= 0', name='ck_margen_ganancia_positive'),
                {'extend_existing': True}
            )

            venta_key = Column(Integer, primary_key=True, autoincrement=True)
            fecha_key = Column(Integer, ForeignKey('DIM_FECHA.fecha_key'), nullable=False)
            producto_key = Column(Integer, ForeignKey('DIM_PRODUCTO.producto_key'), nullable=False)
            cantidad_vendida = Column(Integer, nullable=False)
            precio_unitario = Column(DECIMAL(10, 2), nullable=False)
            descuento_aplicado = Column(DECIMAL(10, 2), default=0.00)
            margen_ganancia = Column(DECIMAL(10, 2), nullable=False)

            def to_dict(self):
                return {
                    "venta_key": self.venta_key,
                    "fecha_key": self.fecha_key,
                    "producto_key": self.producto_key,
                    "cantidad_vendida": self.cantidad_vendida,
                    "precio_unitario": str(self.precio_unitario),
                    "descuento_aplicado": str(self.descuento_aplicado),
                    "margen_ganancia": str(self.margen_ganancia)
                }

        self.FactVentas = FactVentas
