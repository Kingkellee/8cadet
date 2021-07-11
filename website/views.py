from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from blog.models import Post, Category
from django.shortcuts import render
from .models import Leaders, Patron
from .forms import ContactUsForm, AddLeadersForm, AddPatronForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.views.generic import(View, ListView, CreateView)
from newsletter.forms import SubscriptionForm

from blog.models import Post, Category
from comments.models import Comment, Reply





def handler_404(request, exception):
	data = {}
	return render(request, 'website/404.html', data)


def handler_500(request):
	data = {}
	return render(request, 'website/500.html', data)


def index (request):

	sub = SubscriptionForm()
	
	if request.method == 'POST':
		form = ContactUsForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject'],

			body = {
				'name': form.cleaned_data['name'],
				'email': form.cleaned_data['email'],
				'message': form.cleaned_data['message'],
			}

			message = '\n'.join(body.values())
			sender = form.cleaned_data['email']
			recipient = ['kellyiyogun@gmail.com']
			try:
			    send_mail(
			    	subject, 
			    	message,
			    	sender, 
			    	recipient, 
			    	fail_silently=True 
			    )
			    form.save()
			    messages.success(request, 
			    'Your message has been sent successfully, we will get back to you shortly.')
			except BadHeaderError:
				return HttpResponse('Invalid Header found')
			return HttpResponseRedirect(reverse('kolture'))
	else:
		form = ContactUsForm()

	return render (request, 'website/index.html', 
	    { 
	    'form': form,
	    'sub': sub,
	    })



def about (request):
	total_users = User.objects.all().count()
	leaders = Leaders.objects.all().order_by('start_date')
	patrons = Patron.objects.all().order_by('start_date')
	return render (request, 'website/about.html', {
		'total_users': total_users,
		'leaders': leaders,
		'patrons': patrons
		})


def contact(request):
	if request.method == 'POST':
		form = ContactUsForm(request.POST)
		if form.is_valid():
			
			subject = form.cleaned_data['subject'],

			body = {
				'name': form.cleaned_data['name'],
				'email': form.cleaned_data['email'],
				'message': form.cleaned_data['message'],
			}

			message = '\n'.join(body.values())
			sender = form.cleaned_data['email']
			recipient = ['kellyiyogun@gmail.com']

			try:
			    send_mail(
			    	subject, 
			    	message,
			    	sender, 
			    	recipient, 
			    	fail_silently=True 
			    )
			    form.save()
			    messages.success(request, 
			    'Your message has been sent successfully, we will get back to you shortly.')
			except BadHeaderError:
				return HttpResponse('Invalid Header found')
			return HttpResponseRedirect(reverse('contact'))
	else:
		form = ContactUsForm()
	return render (request, 'website/contact.html', {'form': form})


class AuthorPageView(View):
    
	def get(self, request, *args, **kargs):
		users = User.objects.all()
		authors = []
		for user in users:
			user_posts = Post.objects.filter(author=user)
			if user_posts.count() > 0 :
				comments_count = Comment.objects.filter(author=user).count()
				replies_count = Reply.objects.filter(author=user).count()
				comments_count = int(comments_count) + int(replies_count)
				post_counts = user_posts.count()
				authors.append((user, post_counts, comments_count ))

		context = {
		    'authors': authors,
		}

		return render(request, 'website/authors.html', context)
        

class AddLeaders(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):

	model = Leaders
	form_class = AddLeadersForm
	template_name = 'website/add_leader_patron.html'
	success_url = '/adminPanel/dashboard/'
	success_message = "successfully added" 
	
	def test_func(self):
		if self.request.user.is_superuser:
			return True
		return False

	
	def form_valid(self, form):
		form.save()
		return super().form_valid(form)


class AddPatron(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
	
	model = Patron
	form_class = AddPatronForm
	template_name = 'website/add_leader_patron.html'
	success_url = '/adminPanel/dashboard/'
	success_message = "successfully added" 

	def test_func(self):
		if self.request.user.is_superuser:
			return True
		return False

