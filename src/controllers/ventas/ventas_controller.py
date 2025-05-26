from flask import request, jsonify

class VentasController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    # Crear una nueva venta
    def post_venta(self, data):
        fecha_key = data.get('fecha_key')
        producto_key = data.get('producto_key')
        cantidad_vendida = data.get('cantidad_vendida')
        precio_unitario = data.get('precio_unitario')
        descuento_aplicado = data.get('descuento_aplicado', 0.00)
        margen_ganancia = data.get('margen_ganancia')

        # Validaciones básicas
        if not fecha_key or not producto_key or not cantidad_vendida or not precio_unitario or not margen_ganancia:
            return jsonify({"message": "Todos los campos obligatorios son requeridos: fecha_key, producto_key, cantidad_vendida, precio_unitario, margen_ganancia."}), 400

        # Validar que la fecha exista
        fecha_existente = self.models.DIM_FECHA.query.filter_by(fecha_key=fecha_key).first()
        if not fecha_existente:
            return jsonify({"message": "La fecha asociada no existe."}), 404

        # Validar que el producto exista
        producto_existente = self.models.DIM_PRODUCTO.query.filter_by(producto_key=producto_key).first()
        if not producto_existente:
            return jsonify({"message": "El producto asociado no existe."}), 404

        # Crear nueva instancia de venta
        nueva_venta = self.models.FACT_VENTAS(
            fecha_key=fecha_key,
            producto_key=producto_key,
            cantidad_vendida=cantidad_vendida,
            precio_unitario=precio_unitario,
            descuento_aplicado=descuento_aplicado,
            margen_ganancia=margen_ganancia
        )
        try:
            self.getDb().session.add(nueva_venta)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al registrar la venta: {str(e)}"}), 500

        return jsonify({"message": "Venta registrada exitosamente."}), 201

    # Obtener todas las ventas con paginación
    def get_ventas(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        ventas = self.models.FACT_VENTAS.query.paginate(page=page, per_page=per_page, error_out=False)

        if not ventas.items:
            return jsonify({"message": "No hay ventas registradas."}), 404

        return jsonify({
            "ventas": [venta.to_dict() for venta in ventas.items],
            "total": ventas.total,
            "pagina_actual": ventas.page,
            "total_paginas": ventas.pages
        }), 200

    # Obtener una venta por su ID
    def get_venta_id(self, id):
        venta = self.models.FACT_VENTAS.query.filter_by(venta_key=id).first()
        if not venta:
            return jsonify({"message": "Venta no encontrada por el ID proporcionado."}), 404

        return jsonify({
            "fecha_key": venta.fecha_key,
            "producto_key": venta.producto_key,
            "cantidad_vendida": venta.cantidad_vendida,
            "precio_unitario": venta.precio_unitario,
            "descuento_aplicado": venta.descuento_aplicado,
            "monto_total": venta.cantidad_vendida * venta.precio_unitario,
            "monto_final": (venta.cantidad_vendida * venta.precio_unitario) - venta.descuento_aplicado,
            "margen_ganancia": venta.margen_ganancia
        }), 200

    # Actualizar una venta
    def put_venta(self, id, data):
        venta = self.models.FACT_VENTAS.query.filter_by(venta_key=id).first()
        if not venta:
            return jsonify({"message": "Venta no encontrada para actualizar."}), 404

        fecha_key = data.get('fecha_key')
        producto_key = data.get('producto_key')
        cantidad_vendida = data.get('cantidad_vendida')
        precio_unitario = data.get('precio_unitario')
        descuento_aplicado = data.get('descuento_aplicado')
        margen_ganancia = data.get('margen_ganancia')

        # Validaciones
        if fecha_key:
            fecha_existente = self.models.DIM_FECHA.query.filter_by(fecha_key=fecha_key).first()
            if not fecha_existente:
                return jsonify({"message": "La fecha asociada no existe."}), 404

        if producto_key:
            producto_existente = self.models.DIM_PRODUCTO.query.filter_by(producto_key=producto_key).first()
            if not producto_existente:
                return jsonify({"message": "El producto asociado no existe."}), 404

        # Actualizar valores
        venta.fecha_key = fecha_key or venta.fecha_key
        venta.producto_key = producto_key or venta.producto_key
        venta.cantidad_vendida = cantidad_vendida or venta.cantidad_vendida
        venta.precio_unitario = precio_unitario or venta.precio_unitario
        venta.descuento_aplicado = descuento_aplicado or venta.descuento_aplicado
        venta.margen_ganancia = margen_ganancia or venta.margen_ganancia

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar la venta: {str(e)}"}), 500

        return jsonify({"message": "Venta actualizada exitosamente."}), 200

    # Eliminar una venta
    def delete_venta(self, id):
        venta = self.models.FACT_VENTAS.query.filter_by(venta_key=id).first()
        if not venta:
            return jsonify({"message": "Venta no encontrada para eliminar."}), 404

        try:
            self.getDb().session.delete(venta)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar la venta: {str(e)}"}), 500

        return jsonify({"message": "Venta eliminada exitosamente."}), 200
