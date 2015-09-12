# -*- coding: utf-8 -*-
import os, sys
# место, где лежит джанго
#sys.path.append('/home/rad/devel/django-trunk/')
# место, где лежит проект
sys.path.append('/home/tram/pythonix2/')
# файл конфигурации проекта
os.environ['DJANGO_SETTINGS_MODULE'] = 'pythonix2.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

