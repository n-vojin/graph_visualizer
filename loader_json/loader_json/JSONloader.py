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
        def process_node(node_data, parent=None):
            node = add_node(graph, node_data['id'], node_data)

            if parent:
                add_edge(graph, parent, node)

            if 'children' in node_data:
                for child in node_data['children']:
                    process_node(child, node)

            if 'reference' in node_data:
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

        first_key = list(parsed_data.keys())[0]

        for item in parsed_data.get(first_key, []):
            process_node(item)

        return graph