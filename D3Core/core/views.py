import os.path

from django.apps import apps
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.models import Graph, Node, Edge
import jsonpickle
import logging
import json

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html', )


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
        json_data = json_loader.load(
            'F:/skola/FTN/SOIK Softverski obrasci i komponente/GRAPH VISUALIZER/testData.json')  # Replace with actual path

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

        # Prepare the JSON data for download
        json_data = json.dumps(response_data, indent=2, default=str)

        # Create the HttpResponse object with JSON content
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="graph_data.json"'

        logger.info("JSON data prepared for client download")
        return response

    except Exception as e:
        logger.exception(f"Error in get_graph_data: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt  # Remove this if you're using CSRF tokens in production
def visualise(request):
    if request.method == 'POST':

        # Get the visualizer plugins
        visualizer_plugins = apps.get_app_config("core").visualizer_plugins
        simple_visualizer = next((visualizer for visualizer in visualizer_plugins if visualizer.identifier() == "simple_visualizer"), None)

        if not simple_visualizer:
            logger.error("Simple visualizer not found")
            return JsonResponse({"error": "Simple visualizer not found"}, status=400)

        # Your logic here to generate visualization (e.g., HTML content)
        fileString = simple_visualizer.visualize()

        # Return the HTML string as part of the JSON response
        return JsonResponse({'html': fileString})
