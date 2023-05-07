from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import AlumnoModel
from sqlalchemy import func, desc


class Alumnos(Resource):

    def get(self):
        alumnos = db.session.query(AlumnoModel)

        page = 1

        per_page = 10

        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        # devuelve la cantidad de alumnos por cada estado posible (chequear)
        if request.args.get('estado'):
            alumnos = db.session.query(AlumnoModel.estado, func.count(AlumnoModel.id_alumno))\
                        .group_by(AlumnoModel.estado)

        # devuleve todos los alumnos que tienen la planilla medica vencida (NO ANDA)
        if request.args.get('planilla_medica_falso'):
            alumnos = alumnos\
                        .filter(AlumnoModel.planilla_medica == False)

        try:
            alumnos = alumnos.paginate(page=page, per_page=per_page, error_out=True, )
        except:
            return jsonify({"error":"pasame bien las cositas amiguito"})
        
        return jsonify({"alumnos": [alumno.to_json() for alumno in alumnos],
                        "page": page,
                        "pages": alumnos.pages,
                        "total": alumnos.total
                        })

    def post(self):
        alumno = AlumnoModel.from_json(request.get_json())
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json(), 201


class Alumno(Resource):

    def get(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        return alumno.to_json()

    def put(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(alumno, key, value)
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_json(), 201

    def delete(self, id):
        alumno = db.session.query(AlumnoModel).get_or_404(id)
        db.session.delete(alumno)
        db.session.commit()
        return '', 204
