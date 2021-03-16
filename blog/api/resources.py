from blog.models import Post, Tag
from .serializers import PostSerializer, TagSerializer
from .views import DetailView, ListView


class PostApiMixin:
    model = Post
    serializer = PostSerializer


class PostApi(PostApiMixin, DetailView):
    pass


class PostListApi(PostApiMixin, ListView):
    pass


class TagApiMixin:
    model = Tag
    serializer = TagSerializer


class TagApi(TagApiMixin, DetailView):
    pass


class TagListApi(TagApiMixin, ListView):
    pass
