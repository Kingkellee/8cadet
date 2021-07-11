from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed, AtomSiteNewsFeed



urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user-posts'),
    path('', views.PostList.as_view(), name='blog-home'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post-detail'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('like/<slug:slug>', views.like_post, name='like_post'),
    path('edit/<slug:slug>/', views.UpdatePostView.as_view(), name='update_post'),
    path('<slug:slug>/remove', views.DeletePostView.as_view(), name='delete_post'),
    path('category/<int:id>/', views.CategoryView, name='category'),
    path('categorylist/', views.CategoryListView, name='category-list'),
    path('search/results/', views.search, name='search'),
    path('<int:year>/<int:month>/',
         views.ArticleMonthArchiveView.as_view(month_format='%m'),
         name="post_archive_month"),
    

]

