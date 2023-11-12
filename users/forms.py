from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from users.models import User, Reservation
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите имя пользователя или e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        if not get_user_model().objects.filter(username=username).exists():
            raise ValidationError("Неверное имя пользователя или e-mail!")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if not get_user_model().objects.filter(password=password).exists():
            raise ValidationError("Неверный пароль!")
        return password


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
    name = forms.CharField(
        min_length=2,
        error_messages={
            'min_length': 'Минимальная длина имени - 2 символа'
        },
        widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите имя'})
    )
    how_many_people = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите кол-во гостей'}))
    date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': 'form-control py 4', 'placeholder': '19.05.2023 13:00'}))
    table_number = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control py 4', 'placeholder': 'Введите номер столика'}))

    class Meta:
        model = Reservation
        fields = ['name', 'how_many_people', 'table_number', 'date_time']
        read_only = ['time_create']

    def clean_name(self):
        name = self.cleaned_data['name']
        valid_chars = set(
            "' 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдежзи"
            "йклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        )

        if any(char not in valid_chars for char in name):
            raise ValidationError("Имя может содержать только английские, или русские буквы")
        return name

    def clean_table_number(self):
        table_number = self.cleaned_data['table_number']

        if table_number > 10 or table_number < 1:
            raise ValidationError("Пожалуйста, выберите номер столика от 1 до 10")
        return table_number

    def clean_how_many_people(self):
        how_many_people = self.cleaned_data['how_many_people']

        if how_many_people > 10 or how_many_people < 1:
            raise ValidationError("Мимальное кол-во мест 1, максимальное 10")
        return how_many_people


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'style': 'color: black'}))
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={
        'class': 'form-control py 4', 'style': 'color: black'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control py 4'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control py 4'})
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if len(''.join(first_name)) > 20:
            raise ValidationError("Длина имени не должна превышать 20 символов")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if len(''.join(last_name)) > 20:
            raise ValidationError("Длина фамилии не должна превыщать 20 символов")
        return last_name
