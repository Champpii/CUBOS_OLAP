from flask import request, jsonify

class MarcaRoutes:
    """
    Esta clase define las rutas para el recurso Marca.
    """
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        """
        Define las rutas disponibles para el recurso Marca.
        """

        @self.app.route('/ventas/post/marca', methods=['POST'])
        def post_marca():
            """
            Maneja la solicitud POST para registrar una nueva marca.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getMarcaControllers().post_marca(data)

        @self.app.route('/ventas/get/marca', methods=['GET'])
        def get_marcas():
            """
            Maneja la solicitud GET para obtener todas las marcas registradas.
            """
            return self.app_initializer.getMarcaControllers().get_marcas()

        @self.app.route('/ventas/get/marca/<int:id>', methods=['GET'])
        def get_marca_by_id(id):
            """
            Maneja la solicitud GET para obtener una marca por su ID.
            """
            return self.app_initializer.getMarcaControllers().get_marca_id(id)

        @self.app.route('/ventas/put/marca/<int:id>', methods=['PUT'])
        def put_marca(id):
            """
            Maneja la solicitud PUT para actualizar una marca existente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getMarcaControllers().put_marca(id, data)

        @self.app.route('/ventas/delete/marca/<int:id>', methods=['DELETE'])
        def delete_marca(id):
            """
            Maneja la solicitud DELETE para eliminar una marca por su ID.
            """
            return self.app_initializer.getMarcaControllers().delete_marca(id)
