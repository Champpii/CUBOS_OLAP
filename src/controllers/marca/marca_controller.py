from flask import request, jsonify

class MarcaController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    # Crear una nueva marca
    def post_marca(self, data):
        nombre_marca = data.get('nombre_marca')

        if not nombre_marca:
            return jsonify({"message": "El nombre de la marca es obligatorio."}), 400

        marca_existente = self.models.DimMarca.query.filter_by(nombre_marca=nombre_marca).first()
        if marca_existente:
            return jsonify({"message": "La marca ya existe en los registros."}), 409

        nueva_marca = self.models.DimMarca(nombre_marca=nombre_marca)
        try:
            self.getDb().session.add(nueva_marca)
            self.getDb().session.commit()
            return jsonify({"message": "Marca creada exitosamente."}), 201
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear la marca: {str(e)}"}), 500

    # Obtener todas las marcas con paginación (agregado .order_by)
    def get_marcas(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        marcas_query = self.models.DimMarca.query.order_by(self.models.DimMarca.marca_key.asc())
        marcas = marcas_query.paginate(page=page, per_page=per_page, error_out=False)

        if not marcas.items:
            return jsonify({"message": "No hay marcas registradas."}), 404

        return jsonify({
            "marcas": [marca.to_dict() for marca in marcas.items],
            "total": marcas.total,
            "pagina_actual": marcas.page,
            "total_paginas": marcas.pages
        }), 200

    # Obtener una marca por ID
    def get_marca_id(self, id):
        marca = self.models.DimMarca.query.filter_by(marca_key=id).first()
        if not marca:
            return jsonify({"message": "Marca no encontrada por el ID proporcionado."}), 404
        return jsonify(marca.to_dict()), 200

    # Actualizar marca
    def put_marca(self, id, data):
        marca = self.models.DimMarca.query.filter_by(marca_key=id).first()
        if not marca:
            return jsonify({"message": "Marca no encontrada para actualizar."}), 404

        nombre_marca = data.get('nombre_marca')
        if not nombre_marca:
            return jsonify({"message": "El nombre de la marca es obligatorio."}), 400

        marca.nombre_marca = nombre_marca

        try:
            self.getDb().session.commit()
            return jsonify({"message": "Marca actualizada exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar la marca: {str(e)}"}), 500

    # Eliminar marca
    def delete_marca(self, id):
        marca = self.models.DimMarca.query.filter_by(marca_key=id).first()
        if not marca:
            return jsonify({"message": "Marca no encontrada para eliminar."}), 404

        try:
            self.getDb().session.delete(marca)
            self.getDb().session.commit()
            return jsonify({"message": "Marca eliminada exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar la marca: {str(e)}"}), 500
