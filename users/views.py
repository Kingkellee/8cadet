from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect 
from .forms import SignUpForm, PasswordUpdateForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from blog.models import Post
from comments.models import Comment, Reply

# profile update view
@login_required
def Profile_Update(request):
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Profile updated successfully.')  
            return redirect('users:profile_update')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    user_posts = Post.objects.filter(author=request.user)
    comments_count = Comment.objects.filter(author=request.user).count()
    replies_count = Reply.objects.filter(author=request.user).count()
    comments_count = int(comments_count) + int(replies_count)
    post_counts = user_posts.count() 
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'post_counts':post_counts,
        'comments_count':comments_count,
    }
    
    return render(request, 'registration/profile_update.html', context)
    

class PasswordsChangeView(PasswordChangeView):
    # form_class = PasswordUpdateForm
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_updated')
    # success_url = reverse_lazy('blog-home')


def password_updated(request):
    return render(request, 'registration/password_updated.html', {})


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')


