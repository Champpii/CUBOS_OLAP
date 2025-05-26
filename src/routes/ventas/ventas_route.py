from flask import request, jsonify

class VentasRoutes:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/ventas/post/venta', methods=['POST'])
        def post_venta():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getVentasControllers().post_venta(data)

        @self.app.route('/ventas/get/venta', methods=['GET'])
        def get_venta():
            return self.app_initializer.getVentasControllers().get_ventas()

        @self.app.route('/ventas/get/venta/<int:id>', methods=['GET'])
        def get_venta_by_id(id):
            return self.app_initializer.getVentasControllers().get_venta_id(id)

        @self.app.route('/ventas/put/venta/<int:id>', methods=['PUT'])
        def put_venta(id):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getVentasControllers().put_venta(id, data)

        @self.app.route('/ventas/delete/venta/<int:id>', methods=['DELETE'])
        def delete_venta(id):
            return self.app_initializer.getVentasControllers().delete_venta(id)
