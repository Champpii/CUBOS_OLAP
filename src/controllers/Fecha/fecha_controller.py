from flask import request, jsonify

class FechaController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    def post_fecha(self, data):
        required_fields = ['fecha_completa', 'dia', 'dia_semana', 'semana', 'mes', 'trimestre', 'año']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"El campo '{field}' es obligatorio."}), 400

        existing_fecha = self.models.DimFecha.query.filter_by(fecha_completa=data['fecha_completa']).first()
        if existing_fecha:
            return jsonify({"message": "La fecha ya existe en los registros."}), 409

        nueva_fecha = self.models.DimFecha(
            fecha_completa=data['fecha_completa'],
            dia=data['dia'],
            dia_semana=data['dia_semana'],
            semana=data['semana'],
            mes=data['mes'],
            trimestre=data['trimestre'],
            ano=data['año'],
            indicador_fin_semana=data.get('indicador_fin_semana', False),
            indicador_feriado=data.get('indicador_feriado', False)
        )

        try:
            self.db.session.add(nueva_fecha)
            self.db.session.commit()
            return jsonify({"message": "Fecha creada exitosamente."}), 201
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": f"Error al crear la fecha: {str(e)}"}), 500

    def get_fechas(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        query = self.models.DimFecha.query.order_by(self.models.DimFecha.fecha_key)
        fechas = query.paginate(page=page, per_page=per_page, error_out=False)

        if not fechas.items:
            return jsonify({"message": "No hay fechas registradas."}), 404

        return jsonify({
            "fechas": [f.to_dict() for f in fechas.items],
            "total": fechas.total,
            "pagina_actual": fechas.page,
            "total_paginas": fechas.pages
        }), 200

    def get_fecha_id(self, id):
        fecha = self.models.DimFecha.query.filter_by(fecha_key=id).first()
        if not fecha:
            return jsonify({"message": "Fecha no encontrada por el ID proporcionado."}), 404

        return jsonify(fecha.to_dict()), 200

    def put_fecha(self, id, data):
        fecha = self.models.DimFecha.query.filter_by(fecha_key=id).first()
        if not fecha:
            return jsonify({"message": "Fecha no encontrada para actualizar."}), 404

        try:
            for key, value in data.items():
                if hasattr(fecha, key):
                    setattr(fecha, key, value)

            self.db.session.commit()
            return jsonify({"message": "Fecha actualizada exitosamente."}), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": f"Error al actualizar la fecha: {str(e)}"}), 500

    def delete_fecha(self, id):
        fecha = self.models.DimFecha.query.filter_by(fecha_key=id).first()
        if not fecha:
            return jsonify({"message": "Fecha no encontrada para eliminar."}), 404

        try:
            self.db.session.delete(fecha)
            self.db.session.commit()
            return jsonify({"message": "Fecha eliminada exitosamente."}), 200
        except Exception as e:
            self.db.session.rollback()
            return jsonify({"message": f"Error al eliminar la fecha: {str(e)}"}), 500
