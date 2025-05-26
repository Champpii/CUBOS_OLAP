from flask import request, jsonify

class ModeloRoutes:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/ventas/post/modelo', methods=['POST'])
        def post_modelo():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getModeloControllers().post_modelo(data)

        @self.app.route('/ventas/get/modelo', methods=['GET'])
        def get_modelo():
            return self.app_initializer.getModeloControllers().get_modelos()

        @self.app.route('/ventas/get/modelo/<int:id>', methods=['GET'])
        def get_modelo_by_id(id):
            return self.app_initializer.getModeloControllers().get_modelo_id(id)

        @self.app.route('/ventas/put/modelo/<int:id>', methods=['PUT'])
        def put_modelo(id):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getModeloControllers().put_modelo(id, data)

        @self.app.route('/ventas/delete/modelo/<int:id>', methods=['DELETE'])
        def delete_modelo(id):
            return self.app_initializer.getModeloControllers().delete_modelo(id)
