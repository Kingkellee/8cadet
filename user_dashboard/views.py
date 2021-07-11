from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.views.generic import (View, DeleteView,)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post, Category
from taggit.models import Tag


# global setup

def paginate(req ,tag_posts=None, page_num=1):
    paginator = Paginator(posts, page_num) 
    page_number = req.GET.get('page')
    return paginator.get_page(page_number)


def get_posts_cats_tags(req=None, tag_count=3, admin=True):

    cat_tup_list, tag_tup_list = [], []
    if admin:
        posts = Post.objects.filter(status=1).order_by('-created_on')
        categories = list(set([cat for post in posts for cat in post.category.all()]))

        tag_list = Tag.objects.all()
 
        for cat in categories:
                user_post_count = cat.post_set.all().filter(author=req.user).count()
                cat_tup_list.append((cat, user_post_count))
        for tag in tag_list:
            tag_posts = Post.objects.filter(tags=tag).all()
            tag_tuple = (tag, len(tag_posts))
            tag_tup_list.append(tag_tuple)
    else:
        posts = Post.objects.filter(author=req.user, status=1).order_by('-created_on')
        categories = list(set([cat for post in posts for cat in post.category.all()]))

        tag_list = Tag.objects.filter(post__author=req.user)

        for cat in categories:
            user_post_count = cat.post_set.all().filter(author=req.user).count()
            cat_tup_list.append((cat, user_post_count))
        for tag in tag_list:
            tag_posts = Post.objects.filter(tags=tag).all().filter(author=req.user)
            tag_tuple = (tag, len(tag_posts))
            tag_tup_list.append(tag_tuple)
        
    return posts, cat_tup_list, tag_tup_list


class UserDashboard(LoginRequiredMixin, View):

    def get(self, request, *args, **kargs):
        posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=10, admin=False)
        context = {
            'posts': posts,
            'cat_tup_list': cat_tup_list,
            'tag_tup_list': tag_tup_list,
        }
        return render(request, 'user_dashboard/ud_index.html', context)


class DeletePostbyAuthor(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/mydashboard/'
    success_message = 'Post has been Deleted'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeletePostbyAuthor, self).delete(request,*args, **kwargs)



@login_required
def user_dashboard_filter_category_posts_view(request, pk):
    posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=15, admin=False)  
    category = get_object_or_404(Category, pk=pk)
    cat_posts = category.post_set.all().filter(author=request.user)

    context = {
        'posts': cat_posts,
        'category': category,
        'cat_tup_list': cat_tup_list,
        'tag_tup_list': tag_tup_list,
    }

    return render(request, 'user_dashboard/ud_index.html', context)


@login_required
def user_dashboard_filter_tag_posts_view(request, tag):
    posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=15, admin=False)  
    tag_filter_posts = Post.objects.filter(
        tags__name__icontains=tag).all().filter(author=request.user)
    
    page_obj = paginate(request, tag_posts=tag_tup_list, page_num=4)
    
    print (page_obj)
    context = {
        'posts': tag_filter_posts,
        'tag_tup_list': tag_tup_list,
        'cat_tup_list': cat_tup_list,
        'tag': tag,
        'page_obj': page_obj,
    }

    return render(request, 'user_dashboard/ud_index.html', context)


class DraftPostListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kargs):
        posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=10, admin=False)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        draft_post = Post.objects.filter(author=user, status=0).order_by('-created_on')
        context = {
            'draft_post': draft_post,
            'cat_tup_list': cat_tup_list,
            'tag_tup_list': tag_tup_list,
        }
        return render(request, 'user_dashboard/ud_index.html', context)


def publish_post(request, slug=None):
    draft_post = Post.objects.filter(slug=slug, status=0)

    for post in draft_post:
        post.status = 1
        post.save()
        messages.success(request, 'Post has been Published successfully')
        return redirect('user_dashboard')