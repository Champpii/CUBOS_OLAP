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

        # Validaciones básicas
        if not nombre_producto or not modelo_key or not año_fabricacion or not precio_lista or not categoria_key:
            return jsonify({"message": "Los campos obligatorios son requeridos: nombre_producto, modelo_key, año_fabricacion, precio_lista, categoria_key."}), 400

        # Verificar que el modelo exista
        modelo_existente = self.models.DIM_MODELO.query.filter_by(modelo_key=modelo_key).first()
        if not modelo_existente:
            return jsonify({"message": "El modelo asociado no existe."}), 404

        # Verificar que la categoría exista
        categoria_existente = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=categoria_key).first()
        if not categoria_existente:
            return jsonify({"message": "La categoría asociada no existe."}), 404

        # Crear nueva instancia de producto
        nuevo_producto = self.models.DIM_PRODUCTO(
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            modelo_key=modelo_key,
            año_fabricacion=año_fabricacion,
            color=color,
            precio_lista=precio_lista,
            categoria_key=categoria_key
        )
        try:
            self.getDb().session.add(nuevo_producto)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear el producto: {str(e)}"}), 500

        return jsonify({"message": "Producto creado exitosamente."}), 201

    # Obtener todos los productos con paginación
    def get_productos(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        productos = self.models.DIM_PRODUCTO.query.paginate(page=page, per_page=per_page, error_out=False)

        if not productos.items:
            return jsonify({"message": "No hay productos registrados."}), 404

        return jsonify({
            "productos": [producto.to_dict() for producto in productos.items],
            "total": productos.total,
            "pagina_actual": productos.page,
            "total_paginas": productos.pages
        }), 200

    # Obtener un producto por su ID
    def get_producto_id(self, id):
        producto = self.models.DIM_PRODUCTO.query.filter_by(producto_key=id).first()
        if not producto:
            return jsonify({"message": "Producto no encontrado por el ID proporcionado."}), 404

        return jsonify({
            "nombre_producto": producto.nombre_producto,
            "descripcion": producto.descripcion,
            "modelo_key": producto.modelo_key,
            "año_fabricacion": producto.año_fabricacion,
            "color": producto.color,
            "precio_lista": producto.precio_lista,
            "categoria_key": producto.categoria_key
        }), 200

    # Actualizar un producto
    def put_producto(self, id, data):
        producto = self.models.DIM_PRODUCTO.query.filter_by(producto_key=id).first()
        if not producto:
            return jsonify({"message": "Producto no encontrado para actualizar."}), 404

        nombre_producto = data.get('nombre_producto')
        descripcion = data.get('descripcion')
        modelo_key = data.get('modelo_key')
        año_fabricacion = data.get('año_fabricacion')
        color = data.get('color')
        precio_lista = data.get('precio_lista')
        categoria_key = data.get('categoria_key')

        # Validaciones
        if modelo_key:
            modelo_existente = self.models.DIM_MODELO.query.filter_by(modelo_key=modelo_key).first()
            if not modelo_existente:
                return jsonify({"message": "El modelo asociado no existe."}), 404

        if categoria_key:
            categoria_existente = self.models.DIM_CATEGORIA.query.filter_by(categoria_key=categoria_key).first()
            if not categoria_existente:
                return jsonify({"message": "La categoría asociada no existe."}), 404

        # Actualizar valores
        producto.nombre_producto = nombre_producto or producto.nombre_producto
        producto.descripcion = descripcion or producto.descripcion
        producto.modelo_key = modelo_key or producto.modelo_key
        producto.año_fabricacion = año_fabricacion or producto.año_fabricacion
        producto.color = color or producto.color
        producto.precio_lista = precio_lista or producto.precio_lista
        producto.categoria_key = categoria_key or producto.categoria_key

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar el producto: {str(e)}"}), 500

        return jsonify({"message": "Producto actualizado exitosamente."}), 200

    # Eliminar un producto
    def delete_producto(self, id):
        producto = self.models.DIM_PRODUCTO.query.filter_by(producto_key=id).first()
        if not producto:
            return jsonify({"message": "Producto no encontrado para eliminar."}), 404

        try:
            self.getDb().session.delete(producto)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar el producto: {str(e)}"}), 500

        return jsonify({"message": "Producto eliminado exitosamente."}), 200
