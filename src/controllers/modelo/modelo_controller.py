from flask import request, jsonify

class ModeloController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    # Crear un nuevo modelo
    def post_modelo(self, data):
        nombre_modelo = data.get('nombre_modelo')
        año_lanzamiento = data.get('año_lanzamiento')
        marca_key = data.get('marca_key')

        if not nombre_modelo or not año_lanzamiento or not marca_key:
            return jsonify({"message": "Todos los campos son obligatorios."}), 400

        marca_existente = self.models.DimMarca.query.filter_by(marca_key=marca_key).first()
        if not marca_existente:
            return jsonify({"message": "La marca asociada no existe."}), 404

        nuevo_modelo = self.models.DimModelo(
            nombre_modelo=nombre_modelo,
            ano_lanzamiento=año_lanzamiento,
            marca_key=marca_key
        )
        try:
            self.getDb().session.add(nuevo_modelo)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear el modelo: {str(e)}"}), 500

        return jsonify({"message": "Modelo creado exitosamente."}), 201

    # Obtener todos los modelos con paginación (corregido con order_by)
    def get_modelos(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        modelos = self.models.DimModelo.query.order_by(self.models.DimModelo.modelo_key).paginate(
            page=page, per_page=per_page, error_out=False
        )

        if not modelos.items:
            return jsonify({"message": "No hay modelos registrados."}), 404

        return jsonify({
            "modelos": [modelo.to_dict() for modelo in modelos.items],
            "total": modelos.total,
            "pagina_actual": modelos.page,
            "total_paginas": modelos.pages
        }), 200

    def get_modelo_id(self, id):
        modelo = self.models.DimModelo.query.filter_by(modelo_key=id).first()
        if not modelo:
            return jsonify({"message": "Modelo no encontrado por el ID proporcionado."}), 404

        return jsonify({
            "nombre_modelo": modelo.nombre_modelo,
            "año_lanzamiento": modelo.ano_lanzamiento,
            "marca_key": modelo.marca_key
        }), 200

    def put_modelo(self, id, data):
        modelo = self.models.DimModelo.query.filter_by(modelo_key=id).first()
        if not modelo:
            return jsonify({"message": "Modelo no encontrado para actualizar."}), 404

        nombre_modelo = data.get('nombre_modelo')
        año_lanzamiento = data.get('año_lanzamiento')
        marca_key = data.get('marca_key')

        if not nombre_modelo or not año_lanzamiento or not marca_key:
            return jsonify({"message": "Todos los campos son obligatorios para actualizar."}), 400

        marca_existente = self.models.DimMarca.query.filter_by(marca_key=marca_key).first()
        if not marca_existente:
            return jsonify({"message": "La marca asociada no existe."}), 404

        modelo.nombre_modelo = nombre_modelo
        modelo.ano_lanzamiento = año_lanzamiento
        modelo.marca_key = marca_key

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar el modelo: {str(e)}"}), 500

        return jsonify({"message": "Modelo actualizado exitosamente."}), 200

    def delete_modelo(self, id):
        modelo = self.models.DimModelo.query.filter_by(modelo_key=id).first()
        if not modelo:
            return jsonify({"message": "Modelo no encontrado para eliminar."}), 404

        try:
            self.getDb().session.delete(modelo)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar el modelo: {str(e)}"}), 500

        return jsonify({"message": "Modelo eliminado exitosamente."}), 200
