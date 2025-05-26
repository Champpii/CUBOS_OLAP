from flask import request, jsonify

class ModeloRoutes:
    """
    Esta clase define las rutas para el recurso Modelo.
    """
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        """
        Define las rutas disponibles para el recurso Modelo.
        """

        @self.app.route('/ventas/post/modelo', methods=['POST'])
        def post_modelo():
            """
            Maneja la solicitud POST para registrar un nuevo modelo.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getModeloControllers().post_modelo(data)

        @self.app.route('/ventas/get/modelo', methods=['GET'])
        def get_modelos():
            """
            Maneja la solicitud GET para obtener todos los modelos registrados.
            """
            return self.app_initializer.getModeloControllers().get_modelos()

        @self.app.route('/ventas/get/modelo/<int:id>', methods=['GET'])
        def get_modelo_by_id(id):
            """
            Maneja la solicitud GET para obtener un modelo por su ID.
            """
            return self.app_initializer.getModeloControllers().get_modelo_id(id)

        @self.app.route('/ventas/put/modelo/<int:id>', methods=['PUT'])
        def put_modelo(id):
            """
            Maneja la solicitud PUT para actualizar un modelo existente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getModeloControllers().put_modelo(id, data)

        @self.app.route('/ventas/delete/modelo/<int:id>', methods=['DELETE'])
        def delete_modelo(id):
            """
            Maneja la solicitud DELETE para eliminar un modelo por su ID.
            """
            return self.app_initializer.getModeloControllers().delete_modelo(id)
