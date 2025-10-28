from django.apps import AppConfig


class GpsTollAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GPS_Toll_app'

    def ready(self):
        import GPS_Toll_app.signals  # Ensure signals are imported and registered