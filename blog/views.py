from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.dates import MonthArchiveView

from django.contrib import messages
from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.text import slugify
from django.db.models import Q, Count


from .models import Post, Category
from .forms import PostForm

from comments.models import Comment, Reply
from newsletter.forms import SubscriptionForm

from .cats_gen import gen_top_categories
from hitcount.views import HitCountDetailView
from taggit.models import Tag


# global values context processor
def general(request):
    categories = Category.objects.all()
    latest_posts = Post.objects.filter(status=1).order_by('-created_on')[0:3]
    popular_posts =  Post.objects.filter(status=1).order_by('-hit_count_generic__hits')[:4]
    common_tags = Post.tags.most_common()[:10]
    top3_categories = gen_top_categories(categories, 3)
    posts = Post.objects.filter(status=1)
    featured_post = posts.filter(featured=True).order_by('-updated_on')
    form = SubscriptionForm()

    if featured_post:
        featured_post = featured_post[0]
    else:
        if posts:
            featured_post = posts[len(posts)-1]
        else:
            featured_post = None

    return {
        'categories': categories,
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,
        'common_tags': common_tags,
        'top3_categories': top3_categories,
        'featured_post': featured_post,
        'form': form,
    }


def paginate(req ,posts=None, page_num=1):
    paginator = Paginator(posts, page_num) 
    page_number = req.GET.get('page')
    return paginator.get_page(page_number)


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # featured_post = Post.objects.filter(status=2).order_by('-created_on')[:3]
    template_name = 'blog/blog.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        all_posts = Post.objects.filter(status=1).order_by('-created_on')
        context = super(PostList, self).get_context_data(*args, **kwargs)
        context["all_posts"] = all_posts
        # context["form"] = form
        return context


class UserPostListView(generic.ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=author, status=1).order_by('-created_on') 


    def get_context_data(self, *args, **kwargs):
        context = super(UserPostListView, self).get_context_data(*args, **kwargs)
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = Post.objects.filter(author=author, status=1).order_by('-created_on')
        posts_count = posts.count()
        comments_count = Comment.objects.filter(author=author).count()
        replies_count = Reply.objects.filter(author=author).count()
        total_user_comments = int(comments_count) + int(replies_count)
        common_tags = Post.tags.most_common()[:4]
        context["author"] = author
        context["posts_count"] = posts_count
        context["comments_count"] = total_user_comments
        context["post_list"] = posts
        # context["form"] = form
        return context


class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.filter(status=1)
    date_field = "created_on"
    allow_future = True
    template_name = 'blog/post_archive_month.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        all_posts = Post.objects.filter(status=1).order_by('-created_on')
        context = super(ArticleMonthArchiveView, self).get_context_data(*args, **kwargs)
        context["all_posts"] = all_posts
        # context["form"] = form
        return context

   
def like_post(request, slug):

    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, slug=slug)

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())
   

class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    count_hit = True 

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetail, self).get_context_data(*args, **kwargs)
        published = Post.objects.filter(status=1)
        post_draft = Post.objects.filter(status=0)
        query_likes= get_object_or_404(Post, id=self.object.pk)
        total_likes= query_likes.total_likes()
        is_liked = False
        if query_likes.likes.filter(id=self.request.user.id).exists():
            is_liked = True
        context["total_likes"] = total_likes
        context["published"] = published
        context["post_draft"] = post_draft
        context["is_liked"] = is_liked
        context["get_next"] = self.get_queryset().filter(
            pk__gt=self.object.pk, status=1
        ).order_by('pk').first()
        context["get_previous"] = self.get_queryset().filter(
            pk__lt=self.object.pk, status=1
        ).order_by('-pk').first()
        return context


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tag_list = Tag.objects.all()
    tag_posts = Post.objects.filter(
        tags__name__icontains=tag).all()
    page_obj = paginate(request, posts=tag_posts, page_num=2)
    context = {
        'tag': tag,
        'tag_list': tag_list,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_list.html', context)

    
class AddPostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    # form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog-home')
    # fields = '__all__'
    fields = ['title','header_image', 'category', 'content', 'tags', 'status']

    def form_valid(self, form):  
        form.instance.author = self.request.user  
        if form.instance.status == 1:
            messages.success(self.request, 'Post has been Published')
        else:
            messages.success(self.request, 'Post has been saved to Draft')
        
        return super().form_valid(form)


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    template_name= 'blog/category_list.html'
    return render(request, template_name, {'cat_menu_list':cat_menu_list,})


def CategoryView(request, id):

    category = get_object_or_404(Category, id=id)
    posts_in_cat = category.post_set.all()
    page_obj = paginate(request, posts=posts_in_cat, page_num=2)

    return render(request, 'blog/categories.html', {
                        'category_post': posts_in_cat, 
                        'page_obj': page_obj,
                        'cat': category 
                        })


class AddCategoryView(LoginRequiredMixin, generic.View):


    def post(self, request, *args, **kwargs):
        category = request.POST['category']
        categories = Category.objects.all()
        for_not_admin_view = request.POST.get('add_category', 'not_admin')

        if category and category.lower() not in [cat.name.lower() for cat in categories]:
            cat = Category.objects.create(name=category)
            cat.save()
            messages.success(request, f'{category} added as Category')
            if for_not_admin_view == 'add_post_view':
                return redirect('add_post')
            else:
                return redirect('admin-dashboard')
        else:
            messages.error(request, f'{category} is already a Category')
            return redirect('admin-dashboard')


class UpdatePostView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    # form_class = PostForm
    template_name = 'blog/update_post.html'
    success_message = 'Post has be Updated'
    fields = ['title','header_image', 'category', 'content', 'tags', 'status']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    
class DeletePostView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog-home')
    success_message = "Post has been deleted"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        finally:
            Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0).delete()
            messages.success(self.request, self.success_message)
        return super(DeletePostView, self).delete(request,*args, **kwargs)
    

def search (request):
    template_name = 'blog/search_results.html'
    query = request.GET.get('q')

    if query:
        results = Post.objects.filter(
            Q(title__icontains = query) |
            Q(content__icontains = query) 
            ).distinct()
        found = results.count()
        page_obj = paginate(request, posts=results, page_num=20)
    else:
        return HttpResponseRedirect(reverse('blog-home'))

    # page_obj = paginate(request, posts=results, page_num=2)
    
    context = { 
        'page_obj': page_obj,
        'query': query,
        'found': found
    }

    return render(request, template_name, context)

