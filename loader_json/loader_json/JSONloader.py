import json
from core.services.ucitati import LoaderPlugin
from core.models import Graph, Node, Edge, add_node, add_edge


class JSONLoader(LoaderPlugin):
    def naziv(self):
        return "JSON Loader"

    def identifier(self):
        return "json_loader"

    def load(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def map_to_graph(self, parsed_data, graph):
        def process_node(node_data, parent=None, key=None):
            # Generate a unique node ID
            node_id = f"{key}_{id(node_data)}" if key else str(id(node_data))

            # Create node with all data as attributes
            node = add_node(graph, node_id, node_data)

            if parent:
                add_edge(graph, parent, node)

            # Process nested structures
            if isinstance(node_data, dict):
                for key, value in node_data.items():
                    if isinstance(value, (dict, list)):
                        process_node(value, node, key)
            elif isinstance(node_data, list):
                for index, item in enumerate(node_data):
                    if isinstance(item, (dict, list)):
                        process_node(item, node, f"{key}_{index}" if key else str(index))

            # Handle references
            if isinstance(node_data, dict) and 'reference' in node_data:
                references = node_data['reference']
                if isinstance(references, list):
                    for ref in references:
                        ref_node = Node.objects.filter(graph=graph, node_id=ref).first()
                        if ref_node:
                            add_edge(graph, node, ref_node)
                elif isinstance(references, str):
                    ref_node = Node.objects.filter(graph=graph, node_id=references).first()
                    if ref_node:
                        add_edge(graph, node, ref_node)

        # Start processing from the root of the parsed data
        process_node(parsed_data)

        return graph