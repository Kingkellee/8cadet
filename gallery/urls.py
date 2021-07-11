from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path("", views.Albums.as_view(), name='albulms'),
    path("search/", views.PictureSearch.as_view(), name='search'),
    path("tags/<str:tag_name>/", views.PicturesByTags.as_view(), name='tag_name'),
    # all albums
    path("albums/", views.Albums.as_view(), name='albums'),
    # add new album
    path("albums/add/", views.AlbumCreate.as_view(), name='create_album'),
    # pictures by album
    path("albums/<str:album_name>/", views.PicturesByAlbum.as_view(), name='single_album'),
    # upload pictures to album album_name
    path(
        "albums/<str:album_name>/upload/",
        views.PictureUpload.as_view(),
        name="upload_pictures",
    ),
    # delete album album_name
    path("albums/<str:album_name>/delete/", views.AlbumDelete.as_view(), name='delete_album'),
    # update name of the album album_name
    path("albums/<str:album_name>/update/", views.AlbumUpdate.as_view(), name='update_album'),
    # single picture
    path(
        "albums/<str:album_name>/<int:pk>/",
        views.PictureDetails.as_view(),
        name="single_picture",
    ),
    # delete single picture
    path(
        "albums/<str:album_name>/<int:pk>/delete/",
        views.PictureDelete.as_view(),
        name='delete_picture',
    ),
    # update single picture
    path(
        "albums/<str:album_name>/<int:pk>/update/",
        views.PictureUpdate.as_view(),
        name='update_picture',
    ),
]
