from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Название')
    body = TextAreaField('Содержание')
