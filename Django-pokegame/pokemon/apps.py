from django.apps import AppConfig


class PokemonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pokemon'

    def ready(self):
        import pokemon.signals  # noqa: F401 — registers signal handlers