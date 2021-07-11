from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import View, DeleteView, ListView, UpdateView, FormView

from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.db.models import Count

from blog.models import Post, Category
from gallery.models import Album, Picture
from gallery.forms import AlbumForm
from website.models import Leaders, Patron
from website.forms import UpdateLeadersForm, UpdatePatronForm
from user_dashboard.views import get_posts_cats_tags

from taggit.models import Tag


users = User.objects.all()
posts = Post.objects.all().order_by('-created_on')
categories = Category.objects.all()


# view for admin Dashboard home page
class AdminDbView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get(self, request, *args, **kargs):
        global users
        users = users.order_by('date_joined')
        lead_admin = users.filter(is_superuser=True).order_by('date_joined')[0]

        leaders = Leaders.objects.all().order_by('-start_date')
        patrons = Patron.objects.all().order_by('-start_date')

        albums = Album.objects.all()
        pictures = Picture.objects.all() 

        posts, _, tag_tup_list = get_posts_cats_tags(request, tag_count=15)
        featured_posts = posts.filter(featured=True).order_by('-updated_on')
        if featured_posts:
            featured_post = featured_posts[0]
        else:
            featured_post = None

        context = {
            'users': users,
            'posts': posts,
            'albums': albums,
            'pictures': pictures,
            'categories': categories,
            'tag_tup_list': tag_tup_list,
            'featured_post': featured_post,
            'lead_admin': lead_admin,
            'leaders': leaders,
            'patrons': patrons
        }

        return render(request, 'admin_dashboard/admin_site.html', context)


#  admin dashboard all categories view
class ADashAllCategoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = "admin_dashboard/admin_lists.html"
    context_object_name = 'categories'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


#  admin dashboard all tags view
class ADashAllTagView(LoginRequiredMixin, UserPassesTestMixin, View):
    paginate_by=10

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get(self, request, *args, **kargs):
        posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=15)

        context = {
            'tag_tup_list': tag_tup_list,
        }
        return render(request, 'admin_dashboard/admin_list.html', context)



#  admin dashboard all user view
class ADashAllUserView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "admin_dashboard/admin_list.html"
    context_object_name = 'users'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_users = users.order_by('date_joined')
        lead_admin = all_users.filter(is_superuser=True).order_by('date_joined')[0]

        context["lead_admin"] = lead_admin
        return context

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

#  admin dashboard all posts view
class ADashAllPostsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = "admin_dashboard/admin_list.html"
    context_object_name = 'posts'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        featured_posts = Post.objects.filter(featured=True).order_by('-updated_on')
        if featured_posts:
            featured_post = featured_posts[0]
        else:
            featured_post = None

        context["featured_post"] = featured_post
        return context

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

 #  admin dashboard all user view
class ADashAllAlbumView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Album
    template_name = "admin_dashboard/admin_list.html"
    context_object_name = "albums"
    paginate_by = 10
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

#  admin dashboard all posts view
class ADashAllPictureView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Picture
    template_name = "admin_dashboard/admin_list.html"
    context_object_name = 'pictures'
    paginate_by = 10

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

# post that will be deleted from admin dashboard -view
class DeletePostbyAdminView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Successfully deleted.'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        finally:
            Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0).delete()
    

# category that will be deleted from admin dashboard - view
class DeleteCategorybyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Successfully Deleted. '

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# post that will be deleted from admin dashboard -view
class DeleteAlbumbyAdminView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Successfully deleted.'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# picture that will be deleted from admin dashboard -view
class DeletePicturebyAdminView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Successfully deleted.'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        finally:
            Tag.objects.annotate(
                ntag=Count('taggit_taggeditem_items')
            ).filter(ntag=0).delete()

# category update view on admin dashboard - view
class UpdateAlbumbyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'admin_dashboard/update.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Updated Successfully.'
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_object(self):
        return get_object_or_404(Album, name=self.kwargs.get("album_name"))



class UpdatePicturebyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picture
    template_name = 'admin_dashboard/update.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Updated Successfully.'
    fields = ['album', 'picture', 'description']
    # fields = '__all__'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False



# category update view on admin dashboard - view
class UpdateCategorybyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'admin_dashboard/update.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Updated Successfully.'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class UpdateLeaderbyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Leaders
    form_class = UpdateLeadersForm
    template_name = 'website/update.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Updated Successfully.'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class UpdatePatronbyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patron
    form_class = UpdatePatronForm
    template_name = 'website/update.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Updated Successfully.'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False



class DeleteLeaderbyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Leaders
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Successfully Deleted. '

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class DeletePatronbyAdmin(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Patron
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/adminPanel/dashboard/'
    success_message = 'Successfully Deleted. '

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

# super user check fucntion for restricting user -funtion for @user_passes_test decorator
def super_user_check(user):
    if user.is_superuser:
        return True
    else:
        return False



# admin's power to make a post to featured post
@login_required
@user_passes_test(super_user_check)
def make_the_post_featured(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post:
        post.featured = True
        post.save()
        messages.success(request, 'Featured successfully ')
  


@user_passes_test(super_user_check)
def remove_post_featured(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post:
        post.featured = False
        post.save()
        messages.success(request, 'Removed featured successfully ')
        return redirect('admin-dashboard')


#  admin dashboard selected categories's posts view
@login_required
@user_passes_test(super_user_check)
def admin_dashboard_filter_category_posts_view(request, pk):
    global users
    users = users.order_by('date_joined')
    posts, _, tag_tup_list = get_posts_cats_tags(request, tag_count=10)
    category = get_object_or_404(Category, pk=pk)
    cat_posts = category.post_set.all()

    if len(cat_posts) > 0:
        featured_posts = cat_posts.filter(
            featured=True).order_by('-updated_on')
        if featured_posts:
            featured_post = featured_posts[0]
        else:
            featured_post = None
    else:
        posts = None
        featured_post = None

    context = {
        'posts': cat_posts,
        'featured_post': featured_post,
        'category': category,
        'users': users,
        'categories': categories,
        'tag_tup_list': tag_tup_list,
    }

    return render(request, 'admin_dashboard/admin_site.html', context)



#  admin dashboard selected tag's posts view
@login_required
@user_passes_test(super_user_check)
def admin_dashboard_filter_tag_posts_view(request, tag):
    global users
    posts = Post.objects.filter(tags__name__icontains=tag).all()
    users = users.order_by('date_joined')
    _, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=10)

    featured_posts = posts.filter(status=2).order_by('-updated_on')
    # post_draft = Post.objects.filter(status=0)
    # featured = Post.objects.filter(status=2)
    if featured_posts:
        featured_post = featured_posts[0]
    else:
        featured_post = None

    context = {
        'posts': posts,
        'featured_post': featured_post,
        'tag_tup_list': tag_tup_list,
        'users': users,
        'categories': categories,
        'tag': tag,
    }

    return render(request, 'admin_dashboard/admin_site.html', context)



#  admin dashboard selected user's posts view
@login_required
@user_passes_test(super_user_check)
def admin_dashboard_filter_user_posts_view(request, username):
    posts = Post.objects.filter(author__username=username)
    global users
    users = users.order_by('date_joined')
    _, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=10)
    featured_posts = posts.filter(status=2).order_by('-updated_on')
    if featured_posts:
        featured_post = featured_posts[0]
    else:
        featured_post = None

    context = {
        'posts': posts,
        'featured_post': featured_post,
        'user': username,
        'users': users,
        'categories': categories,
        'tag_tup_list': tag_tup_list,
    }

    return render(request, 'admin_dashboard/admin_site.html', context)



# make user as admin view
@login_required
@user_passes_test(super_user_check)
def make_user_as_admin(request, username):
    user = get_object_or_404(User, username=username)

    if not user.is_superuser:
        user.is_staff = True
        user.is_superuser = True
        user.save()
        messages.success(request, f'{user.username} is now admin')

        return redirect('admin-dashboard')
    else:
        messages.error(request, 'Error occured !')
        return redirect('admin-dashboard')



# remove user as admin view
@login_required
@user_passes_test(super_user_check)
def remove_user_admin_as_admin(request, username):
    global users
    admins = users.filter(is_superuser=True).order_by('date_joined')
    lead_admin = admins[0]
    user = get_object_or_404(User, username=username)

    if user.is_superuser and user != lead_admin and user != request.user:
        user.is_superuser = False
        user.is_stuff = False
        user.save()
        messages.success(request, f'{user.username} is removed as admin')
        return redirect('admin-dashboard')
    else:
        messages.error(request, 'Error occured !')
        return redirect('admin-dashboard')



# remove user from database view
@login_required
@user_passes_test(super_user_check)
def remove_user_from_db(request, pk):
    global users
    admins = users.filter(is_superuser=True).order_by('date_joined')
    lead_admin = admins[0]
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        # user = get_object_or_404(User, pk=pk)
        if user != lead_admin and user != request.user:
            user.delete()
            messages.success(request, f'{user.username} removed successfully')
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'Error occured !')
            return redirect('admin-dashboard')

    return render(request, 'admin_dashboard/confirm-delete.html', {'object': user,})
