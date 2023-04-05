from flask_restful import Resource
from flask import request


PROFESORES_CLASES = {
    3: {'nombre': 'Franco', 'apellido': 'Bertoldi', 'clases': ['funcional']},
    4: {'nombre': 'Francisco', 'apellido': 'Lopez Garcia', 'clases': ['powerlifting']}
}


class ProfesoresClases(Resource):
    def get(self):
        return PROFESORES_CLASES

class ProfesorClases(Resource):
    def get(self,id):
        if int(id) in PROFESORES_CLASES:
            return PROFESORES_CLASES[int(id)]
        return '', 404