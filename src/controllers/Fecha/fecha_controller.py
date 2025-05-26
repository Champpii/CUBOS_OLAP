from flask import request, jsonify

class FechaController:
    def __init__(self, db, models):
        self.db = db
        self.models = models

    def getDb(self):
        return self.db

    # Crear una nueva fecha
    def post_fecha(self, data):
        fecha_completa = data.get('fecha_completa')
        dia = data.get('dia')
        dia_semana = data.get('dia_semana')
        semana = data.get('semana')
        mes = data.get('mes')
        trimestre = data.get('trimestre')
        año = data.get('año')
        indicador_fin_semana = data.get('indicador_fin_semana')
        indicador_feriado = data.get('indicador_feriado')

        # Validaciones básicas
        if not fecha_completa or not dia or not dia_semana or not semana or not mes or not trimestre or not año:
            return jsonify({"message": "Todos los campos son obligatorios."}), 400

        # Verificar que la fecha no exista previamente
        existing_fecha = self.models.DIM_FECHA.query.filter_by(fecha_completa=fecha_completa).first()
        if existing_fecha:
            return jsonify({"message": "La fecha ya existe en los registros."}), 409

        # Crear nueva instancia de fecha
        nueva_fecha = self.models.DIM_FECHA(
            fecha_completa=fecha_completa,
            dia=dia,
            dia_semana=dia_semana,
            semana=semana,
            mes=mes,
            trimestre=trimestre,
            año=año,
            indicador_fin_semana=indicador_fin_semana,
            indicador_feriado=indicador_feriado
        )
        try:
            self.getDb().session.add(nueva_fecha)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al crear la fecha: {str(e)}"}), 500

        return jsonify({"message": "Fecha creada exitosamente."}), 201

    # Obtener todas las fechas con paginación
    def get_fechas(self):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        fechas = self.models.DIM_FECHA.query.paginate(page=page, per_page=per_page, error_out=False)

        if not fechas.items:
            return jsonify({"message": "No hay fechas registradas."}), 404

        return jsonify({
            "fechas": [fecha.to_dict() for fecha in fechas.items],
            "total": fechas.total,
            "pagina_actual": fechas.page,
            "total_paginas": fechas.pages
        }), 200

    # Obtener una fecha por su ID
    def get_fecha_id(self, id):
        fecha = self.models.DIM_FECHA.query.filter_by(fecha_key=id).first()
        if not fecha:
            return jsonify({"message": "Fecha no encontrada por el ID proporcionado."}), 404

        return jsonify({
            "fecha_completa": fecha.fecha_completa,
            "dia": fecha.dia,
            "dia_semana": fecha.dia_semana,
            "semana": fecha.semana,
            "mes": fecha.mes,
            "trimestre": fecha.trimestre,
            "año": fecha.año,
            "indicador_fin_semana": fecha.indicador_fin_semana,
            "indicador_feriado": fecha.indicador_feriado
        }), 200

    # Actualizar una fecha
    def put_fecha(self, id, data):
        fecha = self.models.DIM_FECHA.query.filter_by(fecha_key=id).first()
        if not fecha:
            return jsonify({"message": "Fecha no encontrada para actualizar."}), 404

        for key, value in data.items():
            setattr(fecha, key, value)

        try:
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al actualizar la fecha: {str(e)}"}), 500

        return jsonify({"message": "Fecha actualizada exitosamente."}), 200

    # Eliminar una fecha
    def delete_fecha(self, id):
        fecha = self.models.DIM_FECHA.query.filter_by(fecha_key=id).first()
        if not fecha:
            return jsonify({"message": "Fecha no encontrada para eliminar."}), 404

        try:
            self.getDb().session.delete(fecha)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({"message": f"Error al eliminar la fecha: {str(e)}"}), 500

        return jsonify({"message": "Fecha eliminada exitosamente."}), 200
