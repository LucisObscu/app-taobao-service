# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:55:09 2022

@author: tiqmf
"""

import os

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()