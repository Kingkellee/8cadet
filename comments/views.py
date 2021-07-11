from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Comment, Reply
from blog.models import Post

# add comment view
@login_required
def add_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		post_comment = request.POST['post-comment']
		comment = Comment.objects.create(author=request.user, 
		                                 post= post,
		                                 content=post_comment,)
		comment.save()
		messages.success(request, 'Comment Added.')  
		return redirect(reverse('post-detail', kwargs={
		    'slug': post.slug
		}))
	else:
		messages.error(request, 'something went wrong !')
		return redirect('home')
        
# add reply to comment view
@login_required
def reply_comment(request, ppk, cpk):
	post = get_object_or_404(Post, pk=ppk)
	comment = get_object_or_404(Comment, pk=cpk)
	if request.method == 'POST':
		reply_content = request.POST.get('reply_content', None)
		reply = Reply.objects.create(author=request.user, 
	                                     comment = comment,
	                                     reply_content=reply_content,)
		reply.save()
		messages.success(request, 'Replied successfully.')                                          
		return redirect(reverse('post-detail', kwargs={
	        'slug': post.slug
	    }))
	else:
		messages.error(request, 'something gone wrong !')
		return redirect('home')
        

#delete comment view
@login_required
def delete_comment(request, cpk, ppk):
	post = get_object_or_404(Post, pk=ppk)
	comment = get_object_or_404(Comment, pk=cpk)
	if request.method == 'POST':
		if request.user == comment.author or request.user.is_superuser or request.user == post.author:
			comment.delete()
			messages.success(request, 'Comment has been deleted.') 
			return redirect(reverse('post-detail', kwargs={
		        'slug': post.slug
		    }))
		else:
			messages.error(request, 'something went wrong !')
			return redirect(reverse('post-detail', kwargs={
		        'slug': post.slug
		    }))
        
#delete reply view
@login_required
def delete_reply(request, rpk, cpk, ppk):
	post = get_object_or_404(Post, pk=ppk)
	reply = get_object_or_404(Reply, pk=rpk)
	if request.method == 'POST':
		if request.user == reply.author or request.user.is_superuser or request.user == post.author:
			reply.delete()
			messages.success(request, 'Deleted') 
			return redirect(reverse('post-detail', kwargs={
		        'slug': post.slug
		    }))
		else:
			messages.error(request, 'something gone wrong !')
			return redirect(reverse('post-detail', kwargs={
		        'slug': post.slug
		    }))