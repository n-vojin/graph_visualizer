import abc


class UcitatiService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def naziv(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass


class LoaderPlugin(UcitatiService):
    @abc.abstractmethod
    def load(self, file_path):
        """
        Load data from a file and return a parsed structure.
        """
        pass

    @abc.abstractmethod
    def map_to_graph(self, parsed_data, graph):
        """
        Map the parsed data to a Graph object.
        """
        pass


class VisualizerPlugin(UcitatiService):
    @abc.abstractmethod
    def visualize(self):
        """
        Generate a visualization of the graph.
        """
        pass