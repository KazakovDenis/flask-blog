# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from datetime import datetime

from flask import Blueprint, redirect, url_for, request, render_template, flash
from werkzeug.utils import secure_filename

from blog import config
from blog.services.functions import russify
from blog.models import Post, Tag


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def get_cv():
    return render_template('index.html')


@main.route('/notes')
def get_notes():
    posts = Post.query.order_by(Post.created.desc()).all()[:10]
    tags = Tag.query.all()
    return render_template('notes.html', posts=posts, all_tags=tags)


@main.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename, extension = russify(file.filename.rsplit('.', 1)[0]), file.filename.rsplit('.', 1)[-1]

            if extension in config.ALLOWED_EXTENSIONS:
                fn = secure_filename(filename)
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                filename = f'{fn}{timestamp}.{extension}'
                checked_file = str(config.UPLOADS_DIR / filename)
                file.save(checked_file)
                file.close()
                flash('File uploaded')
                return f'/static/uploads/{filename}'    # todo
            else:
                return 'Bad file', 400
        return 'No file', 406
    return redirect(url_for('index'))
