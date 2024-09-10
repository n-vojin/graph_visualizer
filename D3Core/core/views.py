import os.path

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from core.models import Graph, Node, Edge
import logging
import json

logger = logging.getLogger(__name__)


def index(request):
    storage_path = os.path.join(settings.BASE_DIR, 'temp_graph_data.json')
    if os.path.exists(storage_path):
        os.remove(storage_path)
    context = {
        'loader_plugins': apps.get_app_config("core").loader_plugins,
        'visualiser_plugins': apps.get_app_config("core").visualizer_plugins
    }

    return render(request, 'index.html', context )

@csrf_exempt
@require_http_methods(["POST"])
def get_graph_data(request):
    logger.info("get_graph_data view called")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request content type: {request.content_type}")
    logger.info(f"Request POST data: {request.POST}")
    logger.info(f"Request FILES: {request.FILES}")

    # Check if the request has the file
    if 'file' not in request.FILES:
        logger.error("No file in request")
        return JsonResponse({"error": "No file uploaded"}, status=400)

    # Get the loader plugins
    loader_plugins = apps.get_app_config("core").loader_plugins
    json_loader = next((loader for loader in loader_plugins if loader.identifier() == "json_loader"), None)

    if not json_loader:
        logger.error("JSON loader not found")
        return JsonResponse({"error": "JSON loader not found"}, status=400)

    try:
        # Get the uploaded file
        uploaded_file = request.FILES['file']
        logger.info(f"Uploaded file name: {uploaded_file.name}")
        logger.info(f"Uploaded file size: {uploaded_file.size}")

        # Save the uploaded file temporarily
        temp_file_path = default_storage.save('temp_uploads/temp_file.json', ContentFile(uploaded_file.read()))
        temp_file_path = os.path.join(settings.MEDIA_ROOT, temp_file_path)
        logger.info(f"Temporary file saved at: {temp_file_path}")

        # Load the uploaded JSON data
        json_data = json_loader.load(temp_file_path)
        logger.info("JSON data loaded successfully")

        # Create or get a Graph object
        graph_name = "Uploaded Graph"
        graph, created = Graph.objects.get_or_create(name=graph_name)
        logger.info(f"Graph {'created' if created else 'retrieved'}: {graph.name}")

        # Clear existing nodes and edges for this graph
        Node.objects.filter(graph=graph).delete()
        Edge.objects.filter(graph=graph).delete()
        logger.info("Existing nodes and edges cleared")

        # Map the JSON data to the graph
        json_loader.map_to_graph(json_data, graph)
        logger.info("JSON data mapped to graph")

        # Prepare the data for storage
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

        # Save the data to a file on the server
        storage_path = os.path.join(settings.BASE_DIR, 'temp_graph_data.json')
        with open(storage_path, 'w') as f:
            json.dump(response_data, f, indent=2, default=str)

        logger.info(f"Graph data saved to server at: {storage_path}")

        # Clean up the temporary uploaded file
        os.remove(temp_file_path)
        logger.info("Temporary file removed")

        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"Error in get_graph_data: {str(e)}", exc_info=True)
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


@require_http_methods(["GET"])
def fetch_graph_data(request):
    storage_path = os.path.join(settings.BASE_DIR, 'temp_graph_data.json')
    try:
        with open(storage_path, 'r') as f:
            data = json.load(f)

        # Optionally, delete the file after reading
        #os.remove(storage_path)

        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({"error": "Graph data not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid graph data"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)