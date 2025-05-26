from flask import request, jsonify

class VentasRoutes:
    """
    Esta clase define las rutas para el recurso Ventas.
    """
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        """
        Define las rutas disponibles para el recurso Ventas.
        """

        @self.app.route('/ventas/post/venta', methods=['POST'])
        def post_venta():
            """
            Maneja la solicitud POST para registrar una nueva venta.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getVentasControllers().post_venta(data)

        @self.app.route('/ventas/get/venta', methods=['GET'])
        def get_ventas():
            """
            Maneja la solicitud GET para obtener todas las ventas registradas.
            """
            return self.app_initializer.getVentasControllers().get_ventas()

        @self.app.route('/ventas/get/venta/<int:id>', methods=['GET'])
        def get_venta_by_id(id):
            """
            Maneja la solicitud GET para obtener una venta específica por su ID.
            """
            return self.app_initializer.getVentasControllers().get_venta_id(id)

        @self.app.route('/ventas/put/venta/<int:id>', methods=['PUT'])
        def put_venta(id):
            """
            Maneja la solicitud PUT para actualizar los datos de una venta específica.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getVentasControllers().put_venta(id, data)

        @self.app.route('/ventas/delete/venta/<int:id>', methods=['DELETE'])
        def delete_venta(id):
            """
            Maneja la solicitud DELETE para eliminar una venta por su ID.
            """
            return self.app_initializer.getVentasControllers().delete_venta(id)
