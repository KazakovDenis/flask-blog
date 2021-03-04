from sqlalchemy.orm import validates

from blog.factory import db


# TODO: type choices
TYPES = {
    'string': str,
    'integer': int,
    'float': float,
}


class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    group = db.Column(db.String(64), nullable=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(16), default='string')

    @property
    def value(self):
        type_ = TYPES[self.type]
        try:
            return type_(self.content)
        except ValueError:
            return None

    @validates('type')
    def validate_type(self, key, vartype):
        vartype = vartype.lower()
        assert vartype in TYPES
        return vartype
