# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip == '':
            raise forms.ValidationError('Поле username пустое', code='validation_error')
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip == '':
            raise forms.ValidationError('Поле password пустое', code='validation_error')
        return password
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Неверное имя пользователя или пароль1')
        if not user.check_password(password):
            raise forms.ValidationError('Неверное имя пользователя или пароль2')


class SignupForm(forms.Form):
    username = forms.CharField(label='Логин', min_length = 3, max_length=255)
    email = forms.EmailField(label='email')
    password = forms.CharField(label='Пароль', min_length = 6, max_length=255, widget=forms.PasswordInput)
    def clean(self):
        try:
            user = User.objects.get(username = self.cleaned_data['username'])
            if user is not None:
                raise ValidationError('Не правильный логин или пароль')
        except User.DoesNotExist:
            return self.cleaned_data

    def save(self, request):
        logout(request)
        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'])
        user.save()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        login(request, user)
        return user

# class SignupForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)
#     email = forms.CharField(required=False, widget=forms.EmailInput)
#     #email = forms.EmailField(required=False)
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if username.strip == '':
#             raise forms.ValidationError('Поле username пустое', code='validation_error')
#         try:
#             User.objects.get(username=username)
#             raise forms.ValidationError('Введенное имя используется другим пользователем')
#         except User.DoesNotExist:
#             pass
#         return username
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if email.strip == '':
#             raise forms.ValidationError('Поле email пустое', code='validation_error')
#         return email
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         if password.strip == '':
#             raise forms.ValidationError('Поле password пустое', code='validation_error')
#         self.raw_passwrd = password
#         return make_password(password)
#     def save(self):
#         user = User(**self.cleaned_data)
#         user.save()
#         return user


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    def clean(self):
        return self.cleaned_data
    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip() == '':
            raise forms.ValidationError('Поле заголовка пустое', code='validation_error')
        return title
    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Поле вопроса пустое', code='validation_error')
        return text
    # def clean_author(self):
    #     author = self.cleaned_data['author']
    #     user = User.objects.get(id=author)
    #     return user
    def save(self):
        question = Question(**self.cleaned_data)
        # question.author_id = User.objects.get(id=2)
        question.author_id = self._user.id
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError('Поле ответа пустое', code='validation_error')
        return text
    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id = question_id)
        except Question.DoesNotExist:
            raise forms.ValidationError('Неверный id вопроса', code='validation_error')
        return question
    # def clean_author(self):
    #     author = self.cleaned_data['author']
    #     user = User.objects.get(id=author)
    #     return user
    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer

"""
class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    author = forms.IntegerField(widget=forms.HiddenInput)
    def clean_title(self):
        title = self.cleaned_data['title']
        return title
    def clean_text(self):
        text = self.cleaned_data['text']
        return text
    # def clean_author(self):
    #     author = self.cleaned_data['author']
    #     user = User.objects.get(id=author)
    #     return user
    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = self._user.id
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Ask a Question?', )
    author = forms.IntegerField(widget=forms.HiddenInput)
    question = forms.IntegerField(widget=forms.HiddenInput)
    def clean_text(self):
        text = self.cleaned_data['text']
        return text
    def clean_question(self):
        try:
            question_id = self.cleaned_data['question']
            question = Question.objects.get(id=question_id)
            return question
        except models.ObjectDoesNotExist:
            raise forms.ValidationError('Corrupted question id. Try again later.')
    def clean_author(self):
        try:
            author_id = self.cleaned_data['author']
            author = User.objects.get(id=author_id)
            return author
        except models.ObjectDoesNotExist:
            raise forms.ValidationError('Corrupted author id. Try again later.')
    def save(self):
        a = Answer.objects.create(**self.cleaned_data)
        return a
"""