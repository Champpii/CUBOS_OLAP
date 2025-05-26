from flask import request, jsonify

class ProductoRoutes:
    """
    Esta clase define las rutas para el recurso Producto.
    """
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        """
        Define las rutas disponibles para el recurso Producto.
        """

        @self.app.route('/ventas/post/producto', methods=['POST'])
        def post_producto():
            """
            Maneja la solicitud POST para registrar un nuevo producto.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getProductoControllers().post_producto(data)

        @self.app.route('/ventas/get/producto', methods=['GET'])
        def get_productos():
            """
            Maneja la solicitud GET para obtener todos los productos registrados.
            """
            return self.app_initializer.getProductoControllers().get_productos()

        @self.app.route('/ventas/get/producto/<int:id>', methods=['GET'])
        def get_producto_by_id(id):
            """
            Maneja la solicitud GET para obtener un producto por su ID.
            """
            return self.app_initializer.getProductoControllers().get_producto_id(id)

        @self.app.route('/ventas/put/producto/<int:id>', methods=['PUT'])
        def put_producto(id):
            """
            Maneja la solicitud PUT para actualizar un producto existente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "El cuerpo de la solicitud es inválido o está vacío."}), 400
            return self.app_initializer.getProductoControllers().put_producto(id, data)

        @self.app.route('/ventas/delete/producto/<int:id>', methods=['DELETE'])
        def delete_producto(id):
            """
            Maneja la solicitud DELETE para eliminar un producto por su ID.
            """
            return self.app_initializer.getProductoControllers().delete_producto(id)
