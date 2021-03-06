from django.urls import path

from .views import (AdminDbView, DeletePostbyAdminView, UpdatePicturebyAdmin,
                    DeleteCategorybyAdmin, UpdateCategorybyAdmin, DeletePicturebyAdminView,
                    ADashAllAlbumView, ADashAllPictureView, ADashAllPostsView, 
                    ADashAllCategoryView, ADashAllTagView, ADashAllUserView, 
                    UpdateAlbumbyAdmin, DeleteAlbumbyAdminView, UpdateLeaderbyAdmin,
                    DeleteLeaderbyAdmin, UpdatePatronbyAdmin, DeletePatronbyAdmin,
                    
                    make_the_post_featured, remove_post_featured, make_user_as_admin, 
                    remove_user_admin_as_admin, remove_user_from_db,
                    admin_dashboard_filter_user_posts_view, admin_dashboard_filter_tag_posts_view,
                    admin_dashboard_filter_category_posts_view,
                    )

urlpatterns = [
    path("dashboard/", AdminDbView.as_view(), name="admin-dashboard"),
    path("post/<int:pk>/delete", DeletePostbyAdminView.as_view(), name="delete_by_admin"),
    path("dashboard/categories/", ADashAllCategoryView.as_view(), name="dashboard_categories"),
    path("dashboard/tags/", ADashAllTagView.as_view(), name="dashboard_tags"),
    path("dashboard/users/", ADashAllUserView.as_view(), name="dashboard_users"),
    path("dashboard/posts/", ADashAllPostsView.as_view(), name="dashboard_posts"),
    path("dashboard/albums/", ADashAllAlbumView.as_view(), name="dashboard_albums"),
    path("dashboard/pictures/", ADashAllPictureView.as_view(), name="dashboard_pictures"),

    path("album/<str:album_name>/update", UpdateAlbumbyAdmin.as_view(), name="album_update_by_admin"),
    path("album/<int:pk>/delete", DeleteAlbumbyAdminView.as_view(), name="album_delete_by_admin"),

    path("picture/<int:pk>/update", UpdatePicturebyAdmin.as_view(), name="pic_update_by_admin"),
    path("picture/<int:pk>/delete", DeletePicturebyAdminView.as_view(), name="pic_delete_by_admin"),

    path("category/<int:pk>/update", UpdateCategorybyAdmin.as_view(), name="cat_update_by_admin"),
    path("category/<int:pk>/delete", DeleteCategorybyAdmin.as_view(), name="cat_delete_by_admin"),

    path("leader/<int:pk>/update", UpdateLeaderbyAdmin.as_view(), name="leader_update_by_admin"),
    path("leader/<int:pk>/delete", DeleteLeaderbyAdmin.as_view(), name="leader_delete_by_admin"),

    path("patron/<int:pk>/update", UpdatePatronbyAdmin.as_view(), name="patron_update_by_admin"),
    path("patron/<int:pk>/delete", DeletePatronbyAdmin.as_view(), name="patron_delete_by_admin"),


    path("make_featured_post/<slug:slug>/",make_the_post_featured, name="make_feature"),
    path("remove_featured_post/<slug:slug>/",remove_post_featured, name="remove_feature"),
    path("dashboard/categories/<int:pk>/posts/", admin_dashboard_filter_category_posts_view, name="dashboard_category_posts"),
    path("dashboard/tags/<str:tag>/posts/", admin_dashboard_filter_tag_posts_view, name="dashboard_tag_posts"),
    path("dashboard/<str:username>/posts/", admin_dashboard_filter_user_posts_view, name="dashboard_user_posts"),
    path("user/<str:username>/makeasadmin", make_user_as_admin, name="make_user_asadmin"),
    path("user/<str:username>/removeasadmin", remove_user_admin_as_admin, name="remove_user_asadmin"),
    path("user/<int:pk>/remove", remove_user_from_db, name="remove_user"),
]
