from django.apps import AppConfig


class AccessControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_control'

    def ready(self):
        """Ensure GPIO is setup before the app is ready."""
        from access_control.rpi_gpio_conf import setup_gpio

        setup_gpio()
