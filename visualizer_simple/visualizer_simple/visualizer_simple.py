import os.path

from core.services.ucitati import VisualizerPlugin
from django.template import Template


class SimpleVisualizer(VisualizerPlugin):
    def naziv(self):
        return "Simple Visualizer"

    def identifier(self):
        return "simple_visualizer"

    def visualize(self):
        path= os.path.abspath("../visualizer_simple/visualizer_simple/templates/simple_visualizer.html")
        html = open(path).read()

        return html
