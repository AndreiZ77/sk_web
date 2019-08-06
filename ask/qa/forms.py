# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Question, Answer

class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
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
        if self._user.id>=0:
            question.author_id = self._user.id
        else:
            question.author_id = 1
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

    def save(self):
        answer = Answer(**self.cleaned_data)
        if self._user.id >= 0:
            answer.author_id = self._user.id
        else:
            answer.author_id = 1
        answer.save()
        return answer