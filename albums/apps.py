from django.apps import AppConfig
from watson import search as watson

class AlbumsConfig(AppConfig):

    name = 'albums'

    def ready(self):
        models_to_register = ["Album", "Artist", "RecordLabel"]
        for model_name in models_to_register:
            model = self.get_model(model_name)
            watson.register(model)
