from django import forms
from .models import Album, Picture


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("name", "description", )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "required": True,
                    "placeholder": "Album's name...",
                }
            ),

            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "required": True,
                    "placeholder": "Album's description...",
                }
            )
        }

   
class UpdatePictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = "__all__"
    # album = forms.ModelChoiceField(
    #     queryset=Album.objects, empty_label="Select album", label="Album"
    # )
    # picture = forms.ImageField(label="Picture")
    # description = forms.CharField(label="Description", widget=forms.Textarea(attrs={}))
    # tags = forms.CharField(label="Tags")
