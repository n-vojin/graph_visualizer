from django.db import models

class Graph(models.Model):
    """
    Represents a graph structure with nodes and edges.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Node(models.Model):
    """
    Represents a node in the graph.
    """
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, related_name='nodes')
    node_id = models.CharField(max_length=255)
    attributes = models.JSONField(default=dict)

    def __str__(self):
        return f"Node {self.node_id} in {self.graph}"

    class Meta:
        unique_together = ('graph', 'node_id')

class Edge(models.Model):
    """
    Represents an edge between two nodes in the graph.
    """
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, related_name='edges')
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    destination = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')

    def __str__(self):
        return f"Edge from {self.source.node_id} to {self.destination.node_id} in {self.graph}"

    class Meta:
        unique_together = ('graph', 'source', 'destination')

# Helper functions for graph operations

def create_graph(name):
    """
    Creates a new graph.
    """
    return Graph.objects.create(name=name)

def add_node(graph, node_id, attributes=None):
    """
    Adds a new node to the graph.
    """
    return Node.objects.create(graph=graph, node_id=node_id, attributes=attributes or {})

def add_edge(graph, source_node, destination_node):
    """
    Adds a new edge between two nodes in the graph.
    """
    return Edge.objects.create(graph=graph, source=source_node, destination=destination_node)

def remove_node(graph, node_id):
    """
    Removes a node and all its associated edges from the graph.
    """
    Node.objects.filter(graph=graph, node_id=node_id).delete()

def get_root_nodes(graph):
    """
    Returns all nodes in the graph that have no incoming edges.
    """
    return Node.objects.filter(graph=graph, incoming_edges__isnull=True)

def get_node_children(node):
    """
    Returns all children of a given node.
    """
    return Node.objects.filter(graph=node.graph, incoming_edges__source=node)