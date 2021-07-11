from django import forms
from .models import Post, Category
from ckeditor.fields import CKEditorWidget

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        content = forms.CharField(widget=CKEditorWidget())
        fields = ('title','header_image', 'author', 'category', 'content', 'tags', 'status')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id': 'id_author', 'type': 'hidden'}),
            # 'author': forms.Select(attrs={'class': 'form-control', 'value':'', 'id': 'id_author', 'type': 'hidden'}),
            'category': forms.SelectMultiple(choices=choice_list, attrs={'class': 'form-control'}),
            # 'content': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
           
        }
        
    
