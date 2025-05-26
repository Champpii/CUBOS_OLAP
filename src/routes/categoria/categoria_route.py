from flask import request, jsonify

class CategoriaRoutes:
    """
    Esta clase define las rutas para el recurso Categoría.
    """
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        """
        Define las rutas para el recurso categoría.
        """

        @self.app.route('/ventas/get/categorias', methods=['GET'])
        def get_categorias():
            """
            Maneja la solicitud GET para obtener todas las categorías.
            """
            return self.app_initializer.getCategoriaControllers().get_categorias()

        @self.app.route('/ventas/get/categoria/<int:id>', methods=['GET'])
        def get_categoria_id(id):
            """
            Maneja la solicitud GET para obtener una categoría por su ID.
            """
            return self.app_initializer.getCategoriaControllers().get_categoria_id(id)

        @self.app.route('/ventas/post/categoria', methods=['POST'])
        def post_categoria():
            """
            Maneja la solicitud POST para crear una nueva categoría.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getCategoriaControllers().post_categoria(data)

        @self.app.route('/ventas/put/categoria/<int:id>', methods=['PUT'])
        def put_categoria(id):
            """
            Maneja la solicitud PUT para actualizar una categoría existente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getCategoriaControllers().put_categoria(id, data)

        @self.app.route('/ventas/delete/categoria/<int:id>', methods=['DELETE'])
        def delete_categoria(id):
            """
            Maneja la solicitud DELETE para eliminar una categoría.
            """
            return self.app_initializer.getCategoriaControllers().delete_categoria(id)
