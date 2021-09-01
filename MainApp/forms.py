from django.forms import forms, ModelForm, TextInput, Textarea, IntegerField, CharField, ValidationError, PasswordInput
from MainApp.models import Snippet, Comment
from django.contrib.auth.models import User



class SnippetForm(ModelForm):
   class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code', 'public']
       labels = {
           "name": "name", "lang": "language"
       }
       widgets = {
           'name': TextInput(attrs={"class":"red", "placeholder":"Название"})
       }

class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="Password", widget=PasswordInput)
    password2 = CharField(label="Password confirm", widget=PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли должны совпадать")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', "image" ]