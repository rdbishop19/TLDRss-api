from django.apps import AppConfig


class TldrssConfig(AppConfig):
    name = 'tldrss'

    def ready(self):
        from rss_updater import updater
        updater.start()
