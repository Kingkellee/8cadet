from django.urls import path
from . import views


urlpatterns = [
    path("post/<int:pk>/comment/add", views.add_comment, name="add_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/reply",
         views.reply_comment, name="reply_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/delete",
         views.delete_comment, name="delete_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/replies/<int:rpk>/delete",
         views.delete_reply, name="delete_reply"),
    ]
