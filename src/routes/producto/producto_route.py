from flask import request, jsonify

class ProductoRoutes:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/ventas/post/producto', methods=['POST'])
        def post_producto():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getProductoControllers().post_producto(data)

        @self.app.route('/ventas/get/producto', methods=['GET'])
        def get_producto():
            return self.app_initializer.getProductoControllers().get_productos()

        @self.app.route('/ventas/get/producto/<int:id>', methods=['GET'])
        def get_producto_by_id(id):
            return self.app_initializer.getProductoControllers().get_producto_id(id)

        @self.app.route('/ventas/put/producto/<int:id>', methods=['PUT'])
        def put_producto(id):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getProductoControllers().put_producto(id, data)

        @self.app.route('/ventas/delete/producto/<int:id>', methods=['DELETE'])
        def delete_producto(id):
            return self.app_initializer.getProductoControllers().delete_producto(id)
