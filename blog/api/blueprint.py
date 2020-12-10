# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import json
from flask import Blueprint, request, Response

from blog.models import Post, Tag


api = Blueprint('api', __name__, template_folder='templates')
site = 'https://kazakov.ru.net/blog/'
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin, Content-Type',
    'Access-Control-Allow-Methods': 'GET',
}


@api.route('/posts/', methods=['GET', 'OPTIONS'])
def get_posts():

    if request.method == 'OPTIONS':
        response = Response()
        response.headers.extend(headers)
        return response

    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    result = {'posts': {post.title: {
                           'id': post.id,
                           'body': post.body,
                           'created': str(post.created),
                           'URL': site + post.slug,
                           'tags': {tag.name: {'tag.id': tag.id, 'URL': site + 'tag/' + tag.slug}
                                    for tag in post.tags},
                       } for post in posts}}

    result = json.dumps(result)
    response = Response(result, content_type='application/json')
    response.headers.extend(headers)
    return response


@api.route('/tags/', methods=['GET', 'OPTIONS'])
def get_tags():

    if request.method == 'OPTIONS':
        response = Response()
        response.headers.extend(headers)
        return response

    q = request.args.get('q')
    if q:
        tags = Tag.query.filter(Tag.name.contains(q)).order_by(Tag.name.asc())
    else:
        tags = Tag.query.order_by(Tag.name.asc())

    result = {'tags': {tag.name: {
                           'id': tag.id,
                           'posts': {post.title:
                                         {'id': post.id,
                                          'URL': site + post.slug,
                                          'body': post.body}
                                     for post in tag.posts},
                       } for tag in tags}}

    result = json.dumps(result)
    response = Response(result, content_type='application/json')
    response.headers.extend(headers)
    return response
