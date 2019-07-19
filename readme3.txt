***
В результате я добавил класс  в модель  (home/box/web/ask/qa/model.py)
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-added_at')
    def popular(self):
        return self.order_by('-rating')
 а в начало класса Question добавил описание
class Question(models.Model):
        objects = QuestionManager()


*** Andrey Shatilov 2 года назад Ссылка
Если хотите нормальной работы python3 с mysql и у вас при установке django mysqlclient были вот такие оишбки:
sudo apt-get update
sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev
sudo apt-get install python3-dev
sudo pip3 install django mysqlclient

*** Ilnur Ismagilov - 6 месяцев назад
Ссылка
sudo /etc/init.d/mysql start
mysql -uroot -e "create database sk_web;"
mysql -uroot -e "grant all privileges on sk_web.* to 'box'@'localhost' with grant option;"
~/web/ask/manage.py makemigrations
~/web/ask/manage.py migrate


DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sk_web',
        'USER': 'box',
    }
}

from django.contrib.auth.models import User

class QuestionManager(models.Manager):
  def new(self):
    return self.order_by('-added_at')
  def popular(self):
    return self.order_by('-rating')

added_at = models.DateTimeField(auto_now_add=True)

rating = models.IntegerField(default=0)

likes = models.ManyToManyField(User, related_name='question_like_user')

Вроде это все неочевидные места.
По-моему, ужасно сложное задание :(

*** Александр Минеев - 3 года назад
Ссылка
Подытожу:
1. Когда разрабатываете у себя, а потом переносите в тестовый терминал - разрабатывайте в virtualenv и используйте django 1.6. Хорошее подспорье PyCharm.
2. В поле даты используйте auto_now_add=True
3. При создании в модели Questions поле likes типа многие ко многим, но не забудьте указать параметр
related_name='question_like_user', Промежуточное отношение создается автоматически и никакой таблицы Likes создавать вручную не нужно.
4. pymysql ставить не надо, оно установлено. Просто убедитесь что в settings.py правильно указаны параметры соединения
с БД, проверьте ./manage.py dbshell - если все хорошо значит и syncdb пройдет как надо. Не забудьте перед dbshell
и sync запустить mysql.
5. не забудьте qa добавить  в словарь APPLICATIONS settings.py.


*** Михаил Граблевский - 3 года назад
Мои шаги:
1. Клоним проект:
﻿git clone https://github.com/======/ask.git /home/box/web﻿
2. Разбираемся с библиотеками
﻿﻿sudo pip install pymysql # Нужно для работы MySQL
sudo pip install --upgrade django #  ﻿﻿Апргейдим Джангу до последней версии.
3. Настраиваем MySQL
﻿sudo /etc/init.d/mysql start
mysql -u root
CREATE DATABASE stepik CHARACTER SET utf8;
﻿﻿﻿﻿4. Настраиваем Nginx
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
5. Запускаем gunicorn﻿﻿ (из каталога, где у нас лежит wsgi-файл).
cd ﻿~/web/ask/ask﻿
gunicorn -b 0.0.0.0:8000 ask.wsgi:application&
6. Проверка:
﻿curl localhost:8000﻿
Получаем ok.
Что-то опущено (миграции и т.п.). ﻿И не через init.sh. ﻿Но мне бы хоть к отладке приступить по существу задачи, а не из-за проблем с запуском собственно Джанги.
В результате﻿ получаю свою ошибку, о которой писал выше.

*** Iurii Chudnov -   3 года назад
Ссылка
На локальной машине я отлаживался в Django 1.9
В процессе отладки столкнулся с проблемой что модели не применяются к базе данных.
Чтобы это побороть я использовал команду
python manage.py makemigrations qa
﻿После этого использовал команду
python manage.py migrate