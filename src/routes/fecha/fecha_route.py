from flask import request, jsonify

class FechaRoutes:
    """
    Esta clase define las rutas para el recurso Fecha.
    """
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        """
        Define las rutas para el recurso Fecha.
        """

        @self.app.route('/ventas/post/fecha', methods=['POST'])
        def post_fecha():
            """
            Maneja la solicitud POST para registrar una nueva fecha.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getFechaControllers().post_fecha(data)

        @self.app.route('/ventas/get/fecha', methods=['GET'])
        def get_fechas():
            """
            Maneja la solicitud GET para obtener todas las fechas.
            """
            return self.app_initializer.getFechaControllers().get_fechas()

        @self.app.route('/ventas/get/fecha/<int:id>', methods=['GET'])
        def get_fecha_by_id(id):
            """
            Maneja la solicitud GET para obtener una fecha por su ID.
            """
            return self.app_initializer.getFechaControllers().get_fecha_id(id)

        @self.app.route('/ventas/put/fecha/<int:id>', methods=['PUT'])
        def put_fecha(id):
            """
            Maneja la solicitud PUT para actualizar una fecha existente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getFechaControllers().put_fecha(id, data)

        @self.app.route('/ventas/delete/fecha/<int:id>', methods=['DELETE'])
        def delete_fecha(id):
            """
            Maneja la solicitud DELETE para eliminar una fecha por ID.
            """
            return self.app_initializer.getFechaControllers().delete_fecha(id)
