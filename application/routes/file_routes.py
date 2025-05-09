import os
from flask import send_file, Blueprint

# ✅ Define Flask Blueprint for file routes
file_routes = Blueprint("file_routes", __name__)

# ✅ Define APP_DATA_DIR
APP_DATA_DIR = "APP_DATA"

@file_routes.route("/open-file/<path:file_path>")
def serve_file(file_path):
    """Serve files from APP_DATA directory when clicked."""
    full_path = os.path.join(APP_DATA_DIR, file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_file(full_path, as_attachment=False)
    return "File not found", 404

# ✅ Function to register routes
def register_file_routes(server):
    """Registers file serving routes with the Flask server."""
    server.register_blueprint(file_routes)

