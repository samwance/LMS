from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# ��������� ���������� ��������� ��� �������� �������
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

# �������� ���������� ������� Celery
app = Celery('config')

# �������� �������� �� ����� Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# �������������� ����������� � ����������� ����� �� ������ tasks.py � ����������� Django
app.autodiscover_tasks()