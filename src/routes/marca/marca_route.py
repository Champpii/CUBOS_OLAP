from flask import request, jsonify

class MarcaRoutes:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/ventas/post/marca', methods=['POST'])
        def post_marca():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getMarcaControllers().post_marca(data)

        @self.app.route('/ventas/get/marca', methods=['GET'])
        def get_marca():
            return self.app_initializer.getMarcaControllers().get_marcas()

        @self.app.route('/ventas/get/marca/<int:id>', methods=['GET'])
        def get_marca_by_id(id):
            return self.app_initializer.getMarcaControllers().get_marca_id(id)

        @self.app.route('/ventas/put/marca/<int:id>', methods=['PUT'])
        def put_marca(id):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getMarcaControllers().put_marca(id, data)

        @self.app.route('/ventas/delete/marca/<int:id>', methods=['DELETE'])
        def delete_marca(id):
            return self.app_initializer.getMarcaControllers().delete_marca(id)
