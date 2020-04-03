# Only used in Virtual Environment
# Only for deployed code comment it out in local
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
__all__ = ['celery_app']


import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
