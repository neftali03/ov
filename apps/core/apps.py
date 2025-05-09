from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Application configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self):
        """Extend to register custom query lookup."""
        from django.db.models import CharField, Field
        from django.db.models.functions import Length

        from common.models import NotEqual

        Field.register_lookup(NotEqual)
        CharField.register_lookup(Length)
