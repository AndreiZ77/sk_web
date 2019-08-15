from django.urls import path
from . import views

urlpatterns = [
    #home page
    path('', views.question_list, name='question-list'),
    #path('', views.test, name='test'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('question/<int:id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('popular/', views.question_by_rating, name='question-by-rating'),
    path('new/', views.test, name='test'),
]


"""
url(r'^category/(\d+)/$', 'category_view') # захватывается позиционная переменная
url(r'^(?P<pk>\d+)/$', 'post_detail')  # задает имя переменной куда попадет значение
"""