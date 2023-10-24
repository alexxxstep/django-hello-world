from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.http import Http404


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.queryset, self.paginate_by)
        page_number = request.GET.get('page', 1)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            page = paginator.page(1)
        except EmptyPage:
            # If the page is out of range, deliver the last page of results.
            page = paginator.page(paginator.num_pages)

        return render(
            request,
            self.template_name,
            {
                self.context_object_name: page,
                'paginator': paginator,
                'page_obj': page,
            }
        )


def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)

    page_number = request.GET.get('page', 1)
    print('__page_number__', request, page_number)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,

                             )

    return render(request, 'blog/post/detail.html', {'post': post})
