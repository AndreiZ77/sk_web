# nginx
sudo ln -sf /home/box/web/etc/nginx_dj.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

# gunicorn
#sudo ln -s /home/box/web/etc/gunicorn.py /etc/gunicorn.d/gunicorn.py

#cd /home/box/web/ask && sudo gunicorn -b 0.0.0.0:8000 ask.wsgi:app &
cd /home/box/web/ask && gunicorn --bind=0.0.0.0:8000 --workers=2 --timeout=15 --log-level=debug ask.wsgi:application &
#cd /home/box/web && gunicorn -b 0.0.0.0:8080 hello:app &
#sudo gunicorn -c /home/box/web/etc/gunicorn.conf hello:wsgi_application
#sudo gunicorn -c /home/box/web/etc/gunicorn-django.conf ask.wsgi:application

#cd /home/box/web && sudo gunicorn -c /home/box/web/etc/gunicorn.py hello:app

# settings for mysql
#sudo /etc/init.d/mysql start