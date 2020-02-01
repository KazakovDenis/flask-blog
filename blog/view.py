# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from datetime import datetime

from flask import redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

from app import db, Configuration, log, app
from functions import rusify
from models import Post, Tag


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()[:10]
    tags = Tag.query.all()[:50]
    return render_template('index.html', posts=posts, tags=tags)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404


@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename, extension = rusify(file.filename.rsplit('.', 1)[0]), file.filename.rsplit('.', 1)[-1]

            if extension in Configuration.ALLOWED_EXTENSIONS:
                filename = f"{secure_filename(filename)}{datetime.now().strftime('%Y%m%d-%H%M%S')}.{extension}"
                checked_file = os.path.join(Configuration.UPLOAD_FOLDER, filename)
                file.save(checked_file)
                file.close()
                return f'/static/uploads/{filename}'
            else:
                return 'Bad file', 400
        return 'No file', 406
    return redirect(url_for('index'))
