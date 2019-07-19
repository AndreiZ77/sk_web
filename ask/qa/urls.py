from django.urls import path
from . import views

urlpatterns = [
    #home page
    path('', views.test, name='test'),
    path('login/', views.test, name='test'),
    path('signup/', views.test, name='test'),
    path('question/<int:q_id>/', views.test, name='test'),
    path('ask/', views.test, name='test'),
    path('popular/', views.test, name='test'),
    path('new/', views.test, name='test'),
]


"""
url(r'^category/(\d+)/$', 'category_view') # захватывается позиционная переменная
url(r'^(?P<pk>\d+)/$', 'post_detail')  # задает имя переменной куда попадет значение
"""