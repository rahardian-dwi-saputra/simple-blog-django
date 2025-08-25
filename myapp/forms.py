from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Category
from .models import Post
from django.forms import ModelForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'id':'email',
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']
        labels = {
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'password1': 'Password',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id':'first_name',
                'class': 'form-control', 
                'placeholder': 'Nama depan',
                'autocomple':'off'
            }),
            'last_name': forms.TextInput(attrs={
                'id':'last_name',
                'class': 'form-control', 
                'placeholder': 'Nama belakang',
                'autocomple':'off'
            }),
            'username': forms.TextInput(attrs={
                'id':'username',
                'class': 'form-control', 
                'placeholder': 'Username',
                'autocomple':'off'
            })   
        }
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        labels = {
            'name': 'Nama Kategori',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'id':'name',
                'class': 'form-control', 
                'placeholder': 'Nama Kategori',
                'autocomple':'off'
            }),      
        }

    
"""
class CategoryForm(forms.Form):
    name = forms.CharField(
        label='Nama Kategori',
        required=False,
        widget=forms.TextInput(
            attrs={
                'id':'name',
                'class':'form-control',
                'placeholder': 'Nama Kategori',
                'autocomple':'off'
            })
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        #validasi duplikat
        if Category.objects.filter(name=name).exists():
            #self.fields['name'].widget.attrs.update({'class':'form-control is-invalid'})
            self.add_error("name", "Nama Kategori sudah ada")

        #validasi panjang string
        if len(name) < 5:
            #self.fields['name'].widget.attrs.update({'class':'form-control is-invalid'})
            self.add_error("name", "Minimal 5 karakter")
             
        return name
   

class PostForm(forms.Form):
    title = forms.CharField(
        label='Judul',
        required=False,
        widget=forms.TextInput(attrs={
            'id':'title',
            'class':'form-control',
            'placeholder':'Judul',
            'autofocus':'autofocus'
        })
    )
    category_id = forms.ModelChoiceField(
        label='Kategori',
        required=False,
        queryset=Category.objects.all(),
        empty_label="Pilih Kategori",
        widget=forms.Select(attrs={
            'id':'category',
            'class':'form-control'
        })
    )
    is_publish = forms.BooleanField(
        label='Tampilkan?',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'id':'publish',
            'data-toggle':'toggle',
            'data-on':'Ya',
            'data-off':'Tidak',
            'data-onstyle':'success',
            'data-offstyle':'danger',
            'data-size':'sm'
        })
    )
    image = forms.FileField(
        label='Gambar',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class':'form-control-file',
            'id':'image'
        })
    )
    body = forms.CharField(
        label='Isi',
        required=False,
        widget=forms.HiddenInput(attrs={'id':'body'})
    )
     """

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","category_id","is_publish","image","body"]
        labels = {
            'title': 'Judul',
            'category_id':'Kategori',
            'image':'Gambar',
            'is_publish':'Tampilkan?',
            'body':'Isi'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'id':'title',
                'class':'form-control',
                'placeholder':'Judul',
                'autofocus':'autofocus'
            }),
            'category_id': forms.Select(attrs={
                'id':'category',
                'class':'form-control'
            }),
            'is_publish': forms.CheckboxInput(attrs={
                'id':'publish',
                'data-toggle':'toggle',
                'data-on':'Ya',
                'data-off':'Tidak',
                'data-onstyle':'success',
                'data-offstyle':'danger',
                'data-size':'sm'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class':'form-control-file',
                'id':'image'
            }),
            'body': forms.HiddenInput(attrs={
                'id':'body'
            }),  
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_id'].empty_label ="Pilih Kategori"
        self.fields['image'].widget.template_name = 'widget/custom_image_widget.html'