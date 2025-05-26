from flask import request, jsonify
import requests
import uuid

class VentasController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    def validar_por_uuid_primero(self, base_url, uuid_obj, recurso_nombre):
        # 1. Intentar obtener directamente por UUID
        try:
            url = f"{base_url}/{uuid_obj}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True, response.json()
        except Exception as e:
            return False, {"message": f"Error accediendo a {url}: {str(e)}"}

        # 2. Si falla, buscar en páginas
        pagina = 1
        while True:
            try:
                paginated_url = f"{base_url}?page={pagina}"
                response = requests.get(paginated_url, timeout=5)
                if response.status_code != 200:
                    return False, {"message": f"No se pudo consultar {recurso_nombre} paginado"}

                data = response.json()
                lista = data.get(recurso_nombre, [])
                for item in lista:
                    if item.get(f"{recurso_nombre[:-1]}_key") == str(uuid_obj):
                        return True, item

                if pagina >= data.get("total_paginas", 1):
                    break
                pagina += 1
            except Exception as e:
                return False, {"message": f"Error paginando {recurso_nombre}: {str(e)}"}

        return False, {"message": f"{recurso_nombre[:-1].capitalize()} con UUID {uuid_obj} no encontrado."}

    def post_venta(self, data):
        fecha_key = data.get('fecha_key')
        producto_key = data.get('producto_key')
        cantidad_vendida = data.get('cantidad_vendida')
        precio_unitario = data.get('precio_unitario')
        descuento_aplicado = data.get('descuento_aplicado', 0.00)
        margen_ganancia = data.get('margen_ganancia')
        cliente_key = data.get('cliente_key')
        tienda_key = data.get('tienda_key')
        vendedor_key = data.get('vendedor_key')

        if not all([fecha_key, producto_key, cantidad_vendida, precio_unitario, margen_ganancia, cliente_key, tienda_key, vendedor_key]):
            return jsonify({"message": "Faltan campos obligatorios."}), 400

        if not self.models.DimFecha.query.filter_by(fecha_key=fecha_key).first():
            return jsonify({"message": "Fecha no encontrada."}), 404

        if not self.models.DimProducto.query.filter_by(producto_key=producto_key).first():
            return jsonify({"message": "Producto no encontrado."}), 404

        urls = {
            "clientes": "https://autos-flask-umg-backend-ajbqcxhaaudjbdf0.mexicocentral-01.azurewebsites.net/ventas/get/cliente",
            "tiendas": "https://autos-flask-umg-backend-ajbqcxhaaudjbdf0.mexicocentral-01.azurewebsites.net/ventas/get/tienda",
            "vendedores": "https://autos-flask-umg-backend-ajbqcxhaaudjbdf0.mexicocentral-01.azurewebsites.net/ventas/get/vendedor"
        }

        claves = {
            "clientes": cliente_key,
            "tiendas": tienda_key,
            "vendedores": vendedor_key
        }

        for recurso, url in urls.items():
            valido, result = self.validar_por_uuid_primero(url, claves[recurso], recurso)
            if not valido:
                return jsonify({"message": result["message"]}), 404

        nueva_venta = self.models.FactVentas(
            fecha_key=fecha_key,
            producto_key=producto_key,
            cantidad_vendida=cantidad_vendida,
            precio_unitario=precio_unitario,
            descuento_aplicado=descuento_aplicado,
            margen_ganancia=margen_ganancia,
            cliente_key=uuid.UUID(cliente_key),
            tienda_key=uuid.UUID(tienda_key),
            vendedor_key=uuid.UUID(vendedor_key)
        )

        try:
            self.getDb().session.add(nueva_venta)
            self.getDb().session.commit()
            return jsonify({"message": "Venta registrada exitosamente."}), 201
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": str(e)}), 500

    def get_ventas(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        ventas = self.models.FactVentas.query.order_by(self.models.FactVentas.venta_key).paginate(page=page, per_page=per_page, error_out=False)

        if not ventas.items:
            return jsonify({"message": "No hay ventas registradas."}), 404

        return jsonify({
            "ventas": [venta.to_dict() for venta in ventas.items],
            "total": ventas.total,
            "pagina_actual": ventas.page,
            "total_paginas": ventas.pages
        }), 200

    def get_venta_id(self, id):
        venta = self.models.FactVentas.query.filter_by(venta_key=id).first()
        if not venta:
            return jsonify({"message": "Venta no encontrada."}), 404

        return jsonify({
            **venta.to_dict(),
            "monto_total": float(venta.cantidad_vendida) * float(venta.precio_unitario),
            "monto_final": float(venta.cantidad_vendida) * float(venta.precio_unitario) - float(venta.descuento_aplicado),
        }), 200

    def put_venta(self, id, data):
        venta = self.models.FactVentas.query.filter_by(venta_key=id).first()
        if not venta:
            return jsonify({"message": "Venta no encontrada para actualizar."}), 404

        venta.fecha_key = data.get('fecha_key', venta.fecha_key)
        venta.producto_key = data.get('producto_key', venta.producto_key)
        venta.cantidad_vendida = data.get('cantidad_vendida', venta.cantidad_vendida)
        venta.precio_unitario = data.get('precio_unitario', venta.precio_unitario)
        venta.descuento_aplicado = data.get('descuento_aplicado', venta.descuento_aplicado)
        venta.margen_ganancia = data.get('margen_ganancia', venta.margen_ganancia)

        try:
            self.getDb().session.commit()
            return jsonify({"message": "Venta actualizada exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": str(e)}), 500

    def delete_venta(self, id):
        venta = self.models.FactVentas.query.filter_by(venta_key=id).first()
        if not venta:
            return jsonify({"message": "Venta no encontrada para eliminar."}), 404

        try:
            self.getDb().session.delete(venta)
            self.getDb().session.commit()
            return jsonify({"message": "Venta eliminada exitosamente."}), 200
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": str(e)}), 500
