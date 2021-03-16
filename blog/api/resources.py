from blog.models import Post, Tag
from .bases import DetailView, ListView


class PostApiMixin:
    model = Post
    # todo: add tags
    fields = ('id', 'title', 'body', 'created', 'slug')


class PostApi(PostApiMixin, DetailView):
    pass


class PostListApi(PostApiMixin, ListView):
    pass


class TagApiMixin:
    model = Tag
    fields = ('id', 'name', 'slug')


class TagApi(TagApiMixin, DetailView):
    pass


class TagListApi(TagApiMixin, ListView):
    pass
