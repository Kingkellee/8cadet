from django.urls import path, include
from . import views
from newsletter.views import subscription_list


urlpatterns = [
	path('', views.index, name = 'kolture'),
	path('about/', views.about, name = 'about'),
	path('contact/', views.contact, name = 'contact'),
	path('newsletter/subscribe/', subscription_list, name='subscribe'),
	path('authors/', views.AuthorPageView.as_view(), name='authors'),
	path('add_past_leaders/', views.AddLeaders.as_view(), name='add_leaders'),
	path('add_patrons/', views.AddPatron.as_view(), name='add_patrons'),
]

