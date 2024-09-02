from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from core.models import Graph, Node, Edge
import jsonpickle
import logging
import json


logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html',)


@require_http_methods(["GET"])
def get_graph_data(request):
    logger.info("get_graph_data view called")

    # Get the loader plugins
    loader_plugins = apps.get_app_config("core").loader_plugins
    json_loader = next((loader for loader in loader_plugins if loader.identifier() == "json_loader"), None)

    if not json_loader:
        logger.error("JSON loader not found")
        return JsonResponse({"error": "JSON loader not found"}, status=400)

    try:
        # Load your JSON data
        json_data = json_loader.load('F:/skola/FTN/SOIK Softverski obrasci i komponente/GRAPH VISUALIZER/testData.json')  # Replace with actual path

        # Create or get a Graph object
        graph_name = "Test Graph"  # or request.GET.get('graph_name', 'Default Graph')
        graph, created = Graph.objects.get_or_create(name=graph_name)

        # Clear existing nodes and edges for this graph
        Node.objects.filter(graph=graph).delete()
        Edge.objects.filter(graph=graph).delete()

        # Map the JSON data to the graph
        json_loader.map_to_graph(json_data, graph)

        # Prepare the data for the frontend
        nodes = {}
        for node in Node.objects.filter(graph=graph):
            nodes[node.node_id] = {
                "node_id": node.node_id,
                "attributes": node.attributes
            }

        edges = [{"source": {"node_id": edge.source.node_id}, "destination": {"node_id": edge.destination.node_id}}
                 for edge in Edge.objects.filter(graph=graph)]

        response_data = {
            "name": graph.name,
            "nodes": nodes,
            "edges": edges
        }

        return JsonResponse(response_data, json_dumps_params={'default': str})
    except Exception as e:
        logger.exception(f"Error in get_graph_data: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
