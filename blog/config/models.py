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
        return self.get_type()(self.content)

    @validates('type')
    def validate_type(self, key, vartype):
        vartype = vartype.lower()
        choices = ', '.join(TYPES.keys())
        assert vartype in TYPES, f'Incorrect target type, use one of the following: {choices}'
        return vartype

    @validates('content')
    def validate_content(self, key, content):
        type_ = self.get_type()
        try:
            return type_(content)
        except (TypeError, ValueError):
            raise AssertionError(f'Cannot convert "{content}" to "{type_}"')

    def get_type(self):
        return TYPES[self.type]
