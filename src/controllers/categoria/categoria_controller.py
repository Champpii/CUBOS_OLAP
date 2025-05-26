from flask import request, jsonify

class CategoriaController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    def get_categorias(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        try:
            categorias = self.models.DimCategoria.query.order_by(
                self.models.DimCategoria.categoria_key
            ).paginate(page=page, per_page=per_page, error_out=False)
        except Exception as e:
            return jsonify({"message": f"Error al obtener categorías: {str(e)}"}), 500

        if not categorias.items:
            return jsonify({"message": "No hay categorías registradas."}), 404

        return jsonify({
            "categorias": [c.to_dict() for c in categorias.items],
            "total": categorias.total,
            "pagina_actual": categorias.page,
            "total_paginas": categorias.pages
        }), 200

    def get_categoria_id(self, id):
        categoria = self.models.DimCategoria.query.filter_by(categoria_key=id).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada."}), 404

        return jsonify(categoria.to_dict()), 200

    def post_categoria(self, data):
        nombre_categoria = data.get("nombre_categoria")
        descripcion = data.get("descripcion")
        categoria_padre = data.get("categoria_padre")

        if not nombre_categoria:
            return jsonify({"message": "El campo 'nombre_categoria' es obligatorio."}), 400

        nueva_categoria = self.models.DimCategoria(
            nombre_categoria=nombre_categoria,
            descripcion=descripcion,
            categoria_padre=categoria_padre
        )

        try:
            self.getDb().session.add(nueva_categoria)
            self.getDb().session.commit()
            return jsonify({"message": "Categoría creada exitosamente."}), 201
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear la categoría: {str(e)}"}), 500

    def put_categoria(self, id, data):
        categoria = self.models.DimCategoria.query.filter_by(categoria_key=id).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada."}), 404

        nombre_categoria = data.get("nombre_categoria")
        descripcion = data.get("descripcion")
        categoria_padre = data.get("categoria_padre")

        if not nombre_categoria:
            return jsonify({"message": "El campo 'nombre_categoria' es obligatorio."}), 400

        categoria.nombre_categoria = nombre_categoria
        categoria.descripcion = descripcion
        categoria.categoria_padre = categoria_padre

        try:
            self.getDb().session.commit()
            return jsonify({"message": "Categoría actualizada correctamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar la categoría: {str(e)}"}), 500

    def delete_categoria(self, id):
        categoria = self.models.DimCategoria.query.filter_by(categoria_key=id).first()
        if not categoria:
            return jsonify({"message": "Categoría no encontrada."}), 404

        try:
            self.getDb().session.delete(categoria)
            self.getDb().session.commit()
            return jsonify({"message": "Categoría eliminada exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar la categoría: {str(e)}"}), 500
