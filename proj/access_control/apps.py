import logging
import atexit

from django.apps import AppConfig
from access_control.rpi_gpio_conf import get_door

logger = logging.getLogger(__name__)


class AccessControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_control'

    def ready(self):
        """Register `cleanup` with atexit."""
        super().ready()
        #
        #
        logger.info("atexit: registering GPIO cleanup when app is going to shutdown")
        # 1. At start define the instance (singleton) that will be alive always
        self.door = get_door()
        # 2. Register the instance to cleanup
        # This is the only way I found it worked or AttributeError raises.
        atexit.register(self.door.cleanup)
