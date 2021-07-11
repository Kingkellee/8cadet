from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.db.models import Q  # complex lookups (for searching)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
from .models import Album, Picture
from .forms import UpdatePictureForm, AlbumForm


class Albums(ListView):
    model = Album
    template_name = "gallery/gallery.html"
    context_object_name = "albums"
    paginate_by = 18


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = False
        return context


class AlbumDelete(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = "gallery/confirm_delete.html"
    success_url = reverse_lazy("gallery:albums")
    success_message = "Album has been deleted"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    
    def get_object(self):
        return get_object_or_404(Album, name=self.kwargs.get("album_name"))


class AlbumUpdate(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    success_message = "Album has been Updated"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_object(self):
        return get_object_or_404(Album, name=self.kwargs.get("album_name"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


class PictureUpload(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Picture
    template_name = "gallery/upload_pictures_form.html"
    fields = ['album', 'picture']
    success_message = "Uploaded"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_initial(self):
        album = get_object_or_404(Album, name=self.kwargs.get("album_name"))
        return {
            'album': album
        }

    def form_valid(self, form):  
        form.instance.author = self.request.user  
        return super().form_valid(form)


class PictureUpdate(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picture
    template_name = "gallery/update_picture_form.html"
    success_url = reverse_lazy("gallery:albums")
    success_message = 'Updated Successfully.'
    fields = ['album', 'picture', 'description', 'tags']
    # fields = '__all__'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False




class PictureSearch(ListView):
    model = Picture
    context_object_name = "pictures"
    template_name = "gallery/search_pictures.html"
    paginate_by = 1
    ordering = ("-published_date",)

    def get_queryset(self):
        search_query = self.request.GET.get("q", None)
        results = []
        if search_query:
            results = Picture.objects.filter(
                Q(album__name__icontains=search_query)
                | Q(description__icontains=search_query)
            ).distinct()
        return results


class PicturesByAlbum(ListView):
    context_object_name = "pictures"
    template_name = "gallery/pictures_by_album.html"
    paginate_by = 10
    ordering = ("-published_date",)

    def get_queryset(self):
        album = get_object_or_404(Album, name=self.kwargs["album_name"])
        results = []
        if album:
            results = Picture.objects.filter(album__name=album)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs.get("album_name", None)
        # to be implemented
        context["created"] = 0
        return context


class PicturesByTags(ListView):
    model = Picture
    context_object_name = "pictures"
    template_name = "gallery/pictures_by_tags.html"
    paginate_by = 50
    ordering = ("-published_date",)

    def get_queryset(self):
        tag = self.kwargs.get("tag_name", None)
        results = []
        if tag:
            results = Picture.objects.filter(tags__name=tag)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("tag_name", None)
        return context


class PictureDetails(DetailView):
    model = Picture
    template_name = "gallery/single_picture.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs.get("album_name", None)
        context["pk"] = self.kwargs.get("pk", None)
        context["get_next"] = self.get_queryset().filter(
            pk__gt=self.object.pk,
            album__name=self.kwargs.get("album_name", None)
            ).order_by('pk').first()
        context["get_previous"] = self.get_queryset().filter(
            pk__lt=self.object.pk,
            album__name=self.kwargs.get("album_name", None)
            ).order_by('-pk').first()
        return context


class PictureDelete(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Picture
    template_name = "gallery/confirm_delete.html"
    success_url = reverse_lazy("gallery:albums")
    success_message = "Picture has been Deleted"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album_name"] = self.kwargs.get("album_name", None)
        context["pk"] = self.kwargs.get("pk", None)
        return context

