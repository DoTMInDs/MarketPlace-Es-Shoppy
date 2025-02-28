from django.apps import AppConfig


class VenderCenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vender_center'
    
    def ready(self):
        import vender_center.signals
