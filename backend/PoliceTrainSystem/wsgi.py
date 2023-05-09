"""
WSGI config for PoliceTrainSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
import logging
import os

from django.core.wsgi import get_wsgi_application
from face_rec import preload

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PoliceTrainSystem.settings')

application = get_wsgi_application()
logger = logging.getLogger('log')
logger.info('正在启动后端服务')
preload.main()
logger.info('后端服务启动完成')