import json
from django.db import models
from core.models import Graph, Node, Edge, add_node, add_edge
from core.services.ucitati import JSONLoader

# Dummy data examples
dummy_data_1 = {
    "root": {
        "id": "root1",
        "name": "Root Node",
        "children": [
            {
                "id": "child1",
                "name": "Child 1",
                "value": 10
            },
            {
                "id": "child2",
                "name": "Child 2",
                "nested": {
                    "id": "nested1",
                    "name": "Nested Child"
                }
            }
        ]
    }
}

dummy_data_2 = {
    "person": {
        "name": "John Doe",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "Anytown"
        },
        "hobbies": ["reading", "cycling"],
        "family": [
            {
                "relation": "spouse",
                "name": "Jane Doe"
            },
            {
                "relation": "child",
                "name": "Jimmy Doe",
                "age": 5
            }
        ]
    }
}

dummy_data_3 = {
    "project": {
        "name": "Graph Database",
        "tasks": [
            {
                "id": "task1",
                "name": "Design Schema",
                "assigned_to": "Alice",
                "reference": "task2"
            },
            {
                "id": "task2",
                "name": "Implement Backend",
                "assigned_to": "Bob",
                "subtasks": [
                    {"name": "Set up database", "status": "completed"},
                    {"name": "Create API", "status": "in_progress"}
                ]
            }
        ]
    }
}

# Function to print graph structure
def print_graph_structure(graph):
    def print_node(node, level=0):
        print("  " * level + f"Node: {node.node_id}")
        for key, value in node.attributes.items():
            print("  " * (level + 1) + f"{key}: {value}")
        
        children = Node.objects.filter(graph=graph, incoming_edges__source=node)
        for child in children:
            print_node(child, level + 1)

    root_nodes = Node.objects.filter(graph=graph, incoming_edges__isnull=True)
    for root in root_nodes:
        print_node(root)

# Create and populate graphs
loader = JSONLoader()

for i, data in enumerate([dummy_data_1, dummy_data_2, dummy_data_3], 1):
    graph = Graph.objects.create(name=f"Test Graph {i}")
    loader.map_to_graph(data, graph)
    
    print(f"\nGraph structure for Test Graph {i}:")
    print_graph_structure(graph)
    print("\nEdges:")
    for edge in Edge.objects.filter(graph=graph):
        print(f"  {edge.source.node_id} -> {edge.destination.node_id}")
