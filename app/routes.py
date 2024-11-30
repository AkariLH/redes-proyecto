from flask import jsonify
import json
import logging
from flask import Blueprint, request, jsonify, send_file
from app.services.user_service import get_users, add_user, update_user, delete_user
from app.services.router_service import (
    get_all_routers,
    get_router_by_hostname,
    get_interfaces_by_router,
    get_users_by_router,
    add_user_to_router,
    update_user_in_router,
    delete_user_from_router,
)
from app.services.topology_service import (
    scan_network,
    update_topology,
    start_topology_daemon,
    stop_topology_daemon,
    set_daemon_interval,
)
import os


# Crear el Blueprint para todas las rutas
app = Blueprint('app', __name__)

# --- Rutas Generales ---
@app.route('/')
def home():
    return "¡API de Red funcionando correctamente!"

# --- CRUD de Usuarios Global ---
@app.route('/usuarios', methods=['GET'])
def list_users():
    """Obtiene todos los usuarios globales."""
    return jsonify(get_users())

@app.route('/usuarios', methods=['POST'])
def create_user():
    """Crea un nuevo usuario global."""
    data = request.json
    username = data.get("username")
    permissions = data.get("permissions")
    devices = data.get("devices", [])
    return jsonify(add_user(username, permissions, devices))

@app.route('/usuarios/<string:username>', methods=['PUT'])
def modify_user(username):
    """Actualiza un usuario global."""
    data = request.json
    permissions = data.get("permissions")
    devices = data.get("devices")
    user = update_user(username, permissions, devices)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/usuarios/<string:username>', methods=['DELETE'])
def remove_user(username):
    """Elimina un usuario global."""
    return jsonify(delete_user(username))

# --- Gestión de Enrutadores ---
@app.route('/routes', methods=['GET'])
def list_routers():
    """Obtiene todos los enrutadores."""
    return jsonify(get_all_routers())

@app.route('/routers/<string:hostname>', methods=['GET'])
def get_router(hostname):
    """Obtiene un enrutador específico."""
    router = get_router_by_hostname(hostname)
    if router:
        return jsonify(router)
    return jsonify({"error": "Router not found"}), 404

@app.route('/routers/<string:hostname>/interfaces', methods=['GET'])
def get_interfaces(hostname):
    """Obtiene las interfaces de un enrutador específico."""
    interfaces = get_interfaces_by_router(hostname)
    if interfaces:
        return jsonify(interfaces)
    return jsonify({"error": "Router not found or has no interfaces"}), 404

# --- CRUD de Usuarios por Enrutador ---
@app.route('/routers/<string:hostname>/usuarios', methods=['GET'])
def list_users_by_router(hostname):
    """Obtiene los usuarios de un enrutador específico."""
    users = get_users_by_router(hostname)
    if users is not None:
        return jsonify(users)
    return jsonify({"error": "Router not found"}), 404

@app.route('/routers/<string:hostname>/usuarios', methods=['POST'])
def create_user_in_router(hostname):
    """Crea un usuario en un enrutador específico."""
    data = request.json
    username = data.get("username")
    permissions = data.get("permissions")
    user = add_user_to_router(hostname, username, permissions)
    if user is not None:
        return jsonify(user)
    return jsonify({"error": "Router not found"}), 404

@app.route('/routers/<string:hostname>/usuarios', methods=['PUT'])
def update_user_in_router_route(hostname):
    """Actualiza un usuario en un enrutador específico."""
    data = request.json
    username = data.get("username")
    permissions = data.get("permissions")
    user = update_user_in_router(hostname, username, permissions)
    if user is not None:
        return jsonify(user)
    return jsonify({"error": "User or Router not found"}), 404

@app.route('/routers/<string:hostname>/usuarios', methods=['DELETE'])
def delete_user_in_router_route(hostname):
    """Elimina un usuario de un enrutador específico."""
    data = request.json
    username = data.get("username")
    result = delete_user_from_router(hostname, username)
    if result is not None:
        return jsonify(result)
    return jsonify({"error": "Router not found"}), 404

# --- Detección de Topología ---
@app.route('/topologia', methods=['GET'])
def get_topology():
    """
    Devuelve la topología actual desde el archivo.
    """
    try:
        # Leer la topología desde el archivo JSON
        with open("current_topology.json", "r") as f:
            topology = json.load(f)
        logging.debug(f"Topología cargada desde el archivo: {topology}")
        return jsonify(topology)
    except FileNotFoundError:
        logging.error("El archivo de topología no existe.")
        return jsonify([])  # Devuelve vacío si no hay datos aún
    except Exception as e:
        logging.error(f"Error al cargar la topología: {str(e)}")
        return jsonify({"error": "Failed to load topology"}), 500

@app.route('/topologia', methods=['POST'])
def start_topology_detection():
    """
    Inicia un demonio para explorar la topología de red periódicamente.
    """
    data = request.json
    network_range = data.get("network_range", "192.168.1.0/24")
    result = start_topology_daemon(network_range)
    return jsonify(result)

@app.route('/topologia', methods=['PUT'])
def change_daemon_interval():
    """
    Cambia el intervalo de tiempo del demonio.
    """
    data = request.json
    interval = data.get("interval", 300)  # Intervalo por defecto: 5 minutos
    result = set_daemon_interval(interval)
    return jsonify(result)

@app.route('/topologia', methods=['DELETE'])
def stop_topology_detection():
    """
    Detiene el demonio que explora la red.
    """
    result = stop_topology_daemon()
    return jsonify(result)

@app.route('/topologia/graph', methods=['GET'])
def get_topology_graph():
    """
    Genera y devuelve un gráfico de la topología.
    """
    from app.services.topology_service import generate_topology_graph
    graph_path = generate_topology_graph()
    if graph_path and os.path.exists(graph_path):
        return send_file(graph_path, mimetype='image/png')
    else:
        return jsonify({"error": "Failed to generate topology graph"}), 500
