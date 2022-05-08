from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Equipment, Auction, Letter, Profile



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def clean_password2(self):
        # Check that the two password entries match.
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są takie same!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class GorillaForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['information']
        widgets = {
            'information': forms.TextInput(attrs={'class': 'text'}),
        }

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['receiver', 'title', 'content']
