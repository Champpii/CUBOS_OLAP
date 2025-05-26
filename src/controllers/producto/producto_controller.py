from flask import request, jsonify

class ProductoController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    # Crear un nuevo producto
    def post_producto(self, data):
        nombre_producto = data.get('nombre_producto')
        descripcion = data.get('descripcion')
        modelo_key = data.get('modelo_key')
        año_fabricacion = data.get('año_fabricacion')
        color = data.get('color')
        precio_lista = data.get('precio_lista')
        categoria_key = data.get('categoria_key')

        if not nombre_producto or not modelo_key or not año_fabricacion or not precio_lista or not categoria_key:
            return jsonify({"message": "Faltan campos obligatorios."}), 400

        # Validar existencia de modelo y categoría
        if not self.models.DimModelo.query.filter_by(modelo_key=modelo_key).first():
            return jsonify({"message": "El modelo no existe."}), 404

        if not self.models.DimCategoria.query.filter_by(categoria_key=categoria_key).first():
            return jsonify({"message": "La categoría no existe."}), 404

        nuevo_producto = self.models.DimProducto(
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            modelo_key=modelo_key,
            ano_fabricacion=año_fabricacion,
            color=color,
            precio_lista=precio_lista,
            categoria_key=categoria_key
        )

        try:
            self.getDb().session.add(nuevo_producto)
            self.getDb().session.commit()
            return jsonify({"message": "Producto creado exitosamente."}), 201
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear el producto: {str(e)}"}), 500

    # Obtener todos los productos
    def get_productos(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        productos = self.models.DimProducto.query.order_by(self.models.DimProducto.producto_key)\
            .paginate(page=page, per_page=per_page, error_out=False)

        if not productos.items:
            return jsonify({"message": "No hay productos registrados."}), 404

        return jsonify({
            "productos": [p.to_dict() for p in productos.items],
            "total": productos.total,
            "pagina_actual": productos.page,
            "total_paginas": productos.pages
        }), 200

    # Obtener un producto por ID
    def get_producto_id(self, id):
        producto = self.models.DimProducto.query.filter_by(producto_key=id).first()
        if not producto:
            return jsonify({"message": "Producto no encontrado."}), 404

        return jsonify(producto.to_dict()), 200

    # Actualizar un producto
    def put_producto(self, id, data):
        producto = self.models.DimProducto.query.filter_by(producto_key=id).first()
        if not producto:
            return jsonify({"message": "Producto no encontrado para actualizar."}), 404

        modelo_key = data.get('modelo_key')
        categoria_key = data.get('categoria_key')

        if modelo_key and not self.models.DimModelo.query.filter_by(modelo_key=modelo_key).first():
            return jsonify({"message": "El modelo no existe."}), 404

        if categoria_key and not self.models.DimCategoria.query.filter_by(categoria_key=categoria_key).first():
            return jsonify({"message": "La categoría no existe."}), 404

        producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
        producto.descripcion = data.get('descripcion', producto.descripcion)
        producto.modelo_key = modelo_key or producto.modelo_key
        producto.ano_fabricacion = data.get('año_fabricacion', producto.ano_fabricacion)
        producto.color = data.get('color', producto.color)
        producto.precio_lista = data.get('precio_lista', producto.precio_lista)
        producto.categoria_key = categoria_key or producto.categoria_key

        try:
            self.getDb().session.commit()
            return jsonify({"message": "Producto actualizado exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar el producto: {str(e)}"}), 500

    # Eliminar un producto
    def delete_producto(self, id):
        producto = self.models.DimProducto.query.filter_by(producto_key=id).first()
        if not producto:
            return jsonify({"message": "Producto no encontrado para eliminar."}), 404

        try:
            self.getDb().session.delete(producto)
            self.getDb().session.commit()
            return jsonify({"message": "Producto eliminado exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar el producto: {str(e)}"}), 500
