import json
import time  # To measure time
from core.services.ucitati import LoaderPlugin
from core.models import Graph, Node, Edge, add_node, add_edge
from collections import defaultdict


class JSONLoader(LoaderPlugin):
    def naziv(self):
        return "JSON Loader"

    def identifier(self):
        return "json_loader"

    def load(self, file_path):
        start_time = time.time()  # Start time
        with open(file_path, 'r') as file:
            data = json.load(file)
        duration = time.time() - start_time  # End time
        print(f"Loading JSON file took {duration:.4f} seconds")  # Print duration
        return data

    def map_to_graph(self, parsed_data, graph):
        start_time = time.time()  # Start time
        self.graph = graph
        self.node_cache = {}
        self.reference_queue = []
        self.id_counters = defaultdict(int)
        self.process_node(parsed_data)
        self.process_references()
        duration = time.time() - start_time  # End time
        print(f"Mapping to graph took {duration:.4f} seconds")  # Print duration
        return self.graph

    def process_node(self, data, parent_id=None, key=None):
        start_time = time.time()  # Start time
        node_id = self.generate_id(data, key)

        if isinstance(data, dict):
            attributes = {k: v for k, v in data.items() if not isinstance(v, (dict, list))}
            node = add_node(self.graph, node_id, attributes)
            self.node_cache[node_id] = node

            if 'reference' in data:
                self.reference_queue.append((node_id, data['reference']))

            for key, value in data.items():
                if isinstance(value, dict):
                    child_id = self.process_node(value, node_id, key)
                    add_edge(self.graph, node, self.node_cache[child_id])
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, dict):
                            child_id = self.process_node(item, node_id, f"{key}{index + 1}")
                            add_edge(self.graph, node, self.node_cache[child_id])

        elif isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    self.process_node(item, parent_id, f"{key}{index + 1}")

        duration = time.time() - start_time  # End time
        print(f"Processing node '{node_id}' took {duration:.4f} seconds")  # Print duration

        return node_id

    def process_references(self):
        start_time = time.time()  # Start time
        for source_id, references in self.reference_queue:
            source_node = self.node_cache.get(source_id)
            if source_node:
                if isinstance(references, list):
                    for ref in references:
                        target_node = self.node_cache.get(str(ref))
                        if target_node:
                            add_edge(self.graph, source_node, target_node)
                elif isinstance(references, str):
                    target_node = self.node_cache.get(references)
                    if target_node:
                        add_edge(self.graph, source_node, target_node)
        duration = time.time() - start_time  # End time
        print(f"Processing references took {duration:.4f} seconds")  # Print duration

    def generate_id(self, data, key=None):
        start_time = time.time()  # Start time
        if isinstance(data, dict) and 'id' in data:
            return str(data['id'])

        base_id = key or 'root'
        self.id_counters[base_id] += 1
        node_id = f"{base_id}{self.id_counters[base_id]}"
        duration = time.time() - start_time  # End time
        print(f"Generating ID '{node_id}' took {duration:.4f} seconds")  # Print duration

        return node_id
