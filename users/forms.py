from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User, Reservation
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите адрес эл.почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class ReservationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите имя'}))
    how_many_people = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите кол-во гостей'}))
    date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': 'form-control py 4', 'placeholder': '19/05/2023 13:00'}))

    class Meta:
        model = Reservation
        fields = ['name', 'how_many_people', 'date_time']




