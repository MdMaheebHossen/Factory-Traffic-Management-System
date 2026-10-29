from django.apps import AppConfig
import os

class TrafficAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traffic_app'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .traffic_engine import start_engine
            start_engine()