from flask import request, jsonify
from src.models.Models import DimCategoria

class CategoriaController:
    def __init__(self, db):
        self.db = db

    def get_categorias(self):
        categorias = self.db.session.query(DimCategoria).all()
        return jsonify([c.to_dict() for c in categorias]), 200

    def get_categoria_id(self, id):
        categoria = self.db.session.query(DimCategoria).get(id)
        return jsonify(categoria.to_dict()) if categoria else (jsonify({"message": "No encontrada"}), 404)

    def post_categoria(self, data):
        categoria = DimCategoria(**data)
        try:
            self.db.session.add(categoria)
            self.db.session.commit()
            return jsonify({"message": "Categoría creada exitosamente."}), 201
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": str(e)}), 500

    def put_categoria(self, id, data):
        categoria = self.db.session.query(DimCategoria).get(id)
        if not categoria:
            return jsonify({"message": "No encontrada"}), 404
        for key, value in data.items():
            setattr(categoria, key, value)
        try:
            self.db.session.commit()
            return jsonify({"message": "Actualizada correctamente."}), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": str(e)}), 500

    def delete_categoria(self, id):
        categoria = self.db.session.query(DimCategoria).get(id)
        if not categoria:
            return jsonify({"message": "No encontrada"}), 404
        try:
            self.db.session.delete(categoria)
            self.db.session.commit()
            return jsonify({"message": "Eliminada correctamente."}), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": str(e)}), 500