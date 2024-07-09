from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white',
            'placeholder': 'Email or Username',
            'type' : "username"})
        self.fields['password'].widget.attrs.update(
            {'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white mt-5',
            'placeholder': 'Password',
            'type' : "password"})
        

    username = forms.CharField(
        max_length=150
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5',
            'type' : 'text'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5',
            'type' : 'email',
            'placeholder':'example@gmail.com'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-600 focus:border-blue-600 block w-full p-2.5',
            'type' : 'password',
            'placeholder' : "••••••••"
        })

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password"
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model

        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "A user with the Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model

        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with the Email already exists")

        return email

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        #ei pass amr model theke ashe nai. eita client site theke ashche
        # tai self.data er maddhome dhorsi. nahole cleaned_data hoito
        password2 = self.data.get('confirm_password')

        print(password)
        if password != password2:
            raise forms.ValidationError("Password mismatch")

        return password

    def save(self, commit=True, *args, **kwargs):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user

    
