from flask import request, jsonify

class FechaRoutes:
    def __init__(self, app, initializer):
        self.app = app
        self.ctrl = initializer.getFechaControllers()
        self.routes()

    def routes(self):
        @self.app.route('/ventas/post/fecha', methods=['POST'])
        def post_fecha():
            return self.ctrl.post_fecha(request.get_json())

        @self.app.route('/ventas/get/fecha', methods=['GET'])
        def get_fecha():
            return self.ctrl.get_fechas()

        @self.app.route('/ventas/get/fecha/<int:id>', methods=['GET'])
        def get_fecha_by_id(id):
            return self.ctrl.get_fecha_id(id)

        @self.app.route('/ventas/put/fecha/<int:id>', methods=['PUT'])
        def put_fecha(id):
            return self.ctrl.put_fecha(id, request.get_json())

        @self.app.route('/ventas/delete/fecha/<int:id>', methods=['DELETE'])
        def delete_fecha(id):
            return self.ctrl.delete_fecha(id)