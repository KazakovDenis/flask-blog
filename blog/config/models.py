from typing import Optional, Union

from sqlalchemy.orm import validates, Query

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
    type = db.Column(db.String(16), default='string', nullable=False)
    content = db.Column(db.Text, nullable=False)

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
            type_(content)
        except (TypeError, ValueError):
            raise AssertionError(f'Cannot convert "{content}" to "{type_.__name__}"')
        return content

    def get_type(self):
        try:
            return TYPES[self.type]
        except ValueError:
            raise AssertionError('"type" attr should be set before "content"')

    def __repr__(self):
        return f'<Parameter "{self.name}">'


def parameters(name: str = '', group: str = '') -> Union[Query, Optional[Parameter]]:
    """A shortcut to get parameters

    :returns Parameter instance if name set else Parameter Query
    """
    filters = []
    if group:
        filters.append(Parameter.group == group)

    if not name:
        return Parameter.query.filter(*filters).all()

    filters.append(Parameter.name == name)
    return Parameter.query.filter(*filters).first()
