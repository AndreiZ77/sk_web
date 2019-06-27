# nginx
sudo ln -sf /home/box/web/etc/nginx_2.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

# gunicorn
#sudo ln -s /home/box/web/etc/gunicorn.py /etc/gunicorn.d/gunicorn.py
cd /home/box/web && sudo gunicorn -b 0.0.0.0:8080 hello:app &
#cd /home/box/web && sudo gunicorn -c /home/box/web/etc/gunicorn.py hello:app

# settings for mysql
#sudo /etc/init.d/mysql start