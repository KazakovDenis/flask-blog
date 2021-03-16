from blog.models import Post
from .bases import DetailView, ListView


class PostApi(DetailView):
    model = Post


class PostListApi(ListView):
    model = Post
