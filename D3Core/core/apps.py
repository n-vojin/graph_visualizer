import pkg_resources
from django.apps import AppConfig



class D3CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    loader_plugins=[]
    graph = None

    def ready(self):
        self.loader_plugins=load_plugins("loader")

def load_plugins(oznaka):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)

    return plugins
