Прошел задание с использованием python 3.5.3 и django 1.11. Большинство комментариев описывали проблемы, которые возникали, пока проверочная система не была обновлена до последних версий питона и джанги.
Опишу все действия для прохождения этого задания. Надеюсь, кому-нибудь пригодится.
1. Создать проект ask и приложение qa по заданию.
2. Создать тестовый контроллер в файле ask/qa/views.py по заданию.
3. Создать файл ask/qa/urls.py и настроить в нем маршрутизацию. Необходимо, чтобы при любых значениях роута вызывалать одна единственная функция test из ﻿ask/qa/views.py.
4. Настроить маршрутизацию в файле ask/ask/urls.py. Все перечисленные в задании урлы должны ссылаться на ask/qa/urls.py. Например, для URL /login/ это выглядит так: url(r'^login/', include('qa.urls')). Для урла / регулярное выражение будет пустым: r'^$'.
5. Настроить ALLOWED_HOSTS = ['*'] в файле ask/ask/settings.py. Больше я ничего в настройках джанги не менял. DEBUG = True оставлял.
6. Оставить без изменений конфиг gunicorn для hello.py и сам скрипт hello.py.
7. Создать еще один конфиг gunicorn для джанги. От конфига gunicorn для hello.py он отличается портом (как в задании) и значением pythonpath = '/home/box/web/ask'. Не уверен, что вообще прописывать значение pythonpath обязательно; если прописать, все работает. Без pythonpath задание 1.9 не работало, здесь не пробовал.
8. Добавить в конфиг для nginx еще один upstream. Все в конфиге будет два локейшена и два апстрима.
 location ^~ /hello/ отстается без изменений: запросы проксируются на 0.0.0.0:8080.
 location / обрабатывает все запросы, которые не начинаются с /hello/: запросы проксируются на 0.0.0.0:8000.
9. Изменить файл init.sh. Надо запустить сразу два gunicorn с соответствующими конфигами. Все работает без создания символьных ссылок на конфиги gunicorn в папке самого gunicorn и перезапуска gunicorn. Все для gunicron нужны две строки:
 sudo gunicorn -c /home/box/web/etc/gunicorn.conf hello:wsgi_application
 sudo gunicorn -c /home/box/web/etc/gunicorn-django.conf ask.wsgi:application
Вообще, судя по access логам двух gunicorn, в задании не проверяется работа hello.py скрипта. Но в задании сказано, что "старый hello-world скрипт останется работать на порту 8080", поэтому я оставил все для его работы.

Для проверки того, что оба сервера (и ваше простейшее wsgi-приложение, и Django) нормально стартовали, можно использовать команды
curl http://127.0.0.1/hello/?a=bcd
curl http://127.0.0.1/question/123/

python -c "import django; print(django.get_version())"
$pip freeze | grep Django
Django==1.4.3

=====
Долго возился с тестом 4, но все-таки решил.
При запуске init.sh nginx с командой - sudo /etc/init.d/nginx restart - крашился и не запускался.
Запускалось, если прописать в инит.сш вместо этой строки - sudo nginx -c /etc/nginx/sites-enabled/test.conf.
Далее nginx стартует, но выдает ошибки по типу "server" not allowed.
Решил проблему дописыванием в свой nginx.conf следующей структуры:

user www-data;
worker_processes 4;
pid /run/nginx.pid;

events {
       worker_connections 768;
}

http {
      server {
        Здесь ваши настройки сервера
     }
}


И еще по проверке на работоспособность:
curl -vv 127.0.0.1:8080/?a=b - запрос отправляется напрямую к gunicorn
curl -vv 127.0.0.1/hello/?a=b - проверяем работает и проксирует ли nginx


=====
@Anonymous_15370114 из предыдущей задачи я с таким конфигом смог запустить - может поможет:
CONFIG = {
    'mode': 'wsgi',
    'working_dir': '/home/box/web',

    'python': '/usr/bin/python',
    'args': (
        '--bind=0.0.0.0:8080',
        '--workers=4',

        '--timeout=60',
      '--daemon',
        'hello:application',
    ),
}
конфиг у меня такой же(только без mode, python и --daemon). Проблема только в том, что на моей виртуалке с конфигом не стартует, надо запускать из консоли. А на виртуалке курса все нормально, запускается с конфига.


=====
Пришлось в итоге делать не совсем так, как говорится в инструкции.
Сделайте следующие шаги, что бы не было головной боли у вас:

virtualenv -p python3 myvenv
source myvenv/bin/activate
pip install --upgrade pip
pip install django
pip install gunicorn

После этого можно стартовать gunicorn:
cd /home/box/web/ask
gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=15 --log-level=debug ask.wsgi:application

=====
Bakytzhan Bektugan
год назад
Ссылка
Не знаю проходит ли кто курс сейчас, потому что последнему комментарию уже год. Хотел бы добавить от себя следующее:

1) Обновляем сразу django (sudo pip3 install --upgrade django). Сейчас в виртуальной машине стоит Python 3.4.3 и
это вполне подходит для Django 2.0.7, поэтому python не обновляем.
2) В файле web/ask/ask/settings.py в INSTALLED_APPS добавляем наши приложения qa и ask, изменим ALLOWED_HOSTS = ['*']
и DEBUG = True.
3) Все пути в ask/ask/urls.py я писал через path, а не через url. Не хотел писать через url, потому что они
являются устаревшими. Например, так выглядит path для  /question/<123>/:
 path('question/<int:id>/', views.test, name='question'). Не забудьте импортировать views из qa.
 Все это можно сделать вторым способом как писал @Николай Гурьев создав второй urls.py в web/ask/ask/qa и
 ссылаясь на него через include(). Но в задании так не сказано.

4) Судя по комментариям многие настраивают Gunicorn через конфигурационные файлы. По документации это должно быть
обычным python файлом. Для Django я написал django_conf.py, и добавил в init.sh:
  sudo ln -sf /home/box/web/etc/django_conf.py /etc/gunicorn.d/django_conf.py
  sudo gunicorn -c /etc/gunicorn.d/django_conf.py ask.wsgi:application
Старый hello.py я просто удалил.

5)Про nginx написано достаточно. Там просто надо настроить location /.