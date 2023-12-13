from .. import db

profesores_clases = db.Table("profesores_clases",
                             db.Column("id_profesor_clase", db.Integer, primary_key=True),
                             db.Column("id_clase", db.Integer, db.ForeignKey("clase.id_clase")),
                             db.Column("id_profesor", db.Integer, db.ForeignKey("profesor.id_profesor")))


class Profesor(db.Model):
    __tablename__ = "profesor"

    id_profesor = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

    certificacion = db.Column(db.String(45), nullable=False)
    fecha_inicio_actividad = db.Column(db.String(45), nullable=False)
    sueldo = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(45), nullable=False)
    aprobacion_pendiente = db.Column(db.Boolean, nullable=False, default=True)

    usuario = db.relationship('Usuario', back_populates='profesor', uselist=False, cascade="all, delete-orphan",
                              single_parent=True)
    clases = db.relationship('Clase', secondary=profesores_clases, backref=db.backref('profesores_p', lazy='dynamic'),
                             lazy='dynamic', overlaps="clases,profesores_p")

    def __repr__(self):
        return '<profesor: %r >' % (self.id_profesor)

    def to_json(self):
        profesor_json = {
            'id_profesor': self.id_profesor,
            'certificacion': self.certificacion,
            'fecha_inicio_actividad': self.fecha_inicio_actividad,
            'sueldo': str(self.sueldo),
            'estado': self.estado,
            'aprobacion_pendiente': self.aprobacion_pendiente,
        }
        return profesor_json

    def to_json_complete(self):
        profesor_json = {
            'id_profesor': str(self.id_profesor),
            'id_usuario': self.id_usuario,
            'nombre': self.usuario.nombre,
            'apellido': self.usuario.apellido,
            'edad': self.usuario.edad,
            'certificacion': self.certificacion,
            'fecha_inicio_actividad': self.fecha_inicio_actividad,
            'sueldo': str(self.sueldo),
            'estado': self.estado,
            "clases": [clase.to_json() for clase in self.clases],
            'aprobacion_pendiente': self.aprobacion_pendiente,
        }
        return profesor_json

    @staticmethod
    def from_json(profesor_json):
        id_profesor = profesor_json.get('id_profesor')
        id_usuario = profesor_json.get('id_usuario')
        certificacion = profesor_json.get('certificacion')
        fecha_inicio_actividad = profesor_json.get('fecha_inicio_actividad')
        sueldo = profesor_json.get('sueldo')
        estado = profesor_json.get('estado')
        aprobacion_pendiente = profesor_json.get('aprobacion_pendiente')
        return Profesor(id_profesor=id_profesor,
                        id_usuario=id_usuario,
                        certificacion=certificacion,
                        fecha_inicio_actividad=fecha_inicio_actividad,
                        sueldo=sueldo,
                        estado=estado,
                        aprobacion_pendiente=aprobacion_pendiente
                        )
