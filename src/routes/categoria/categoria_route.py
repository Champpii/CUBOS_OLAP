from flask import request, jsonify
from src.models.Models import DimCategoria

class CategoriaRoutes:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/ventas/get/categorias', methods=['GET'])
        def get_categorias():
            return self.app_initializer.getCategoriaControllers().get_categorias()

        @self.app.route('/ventas/get/categoria/<int:id>', methods=['GET'])
        def get_categoria_id(id):
            return self.app_initializer.getCategoriaControllers().get_categoria_id(id)

        @self.app.route('/ventas/post/categoria', methods=['POST'])
        def post_categoria():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getCategoriaControllers().post_categoria(data)

        @self.app.route('/ventas/put/categoria/<int:id>', methods=['PUT'])
        def put_categoria(id):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getCategoriaControllers().put_categoria(id, data)

        @self.app.route('/ventas/delete/categoria/<int:id>', methods=['DELETE'])
        def delete_categoria(id):
            return self.app_initializer.getCategoriaControllers().delete_categoria(id)
