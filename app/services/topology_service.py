import nmap
import threading
import time
import logging
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from threading import Event

# Configurar logging para depuración
logging.basicConfig(level=logging.DEBUG)

# Variables globales para el manejo del demonio y la topología
current_topology = []  # Almacena la topología actual
daemon_running = False  # Indica si el demonio está activo
daemon_interval = 300  # Intervalo por defecto: 5 minutos (en segundos)
daemon_thread = None  # Hilo del demonio
stop_event = Event()  # Evento para controlar la detención del demonio

def scan_network(network_range):
    """
    Escanea la red para detectar dispositivos activos.
    :param network_range: Rango de red (e.g., "192.168.56.0/24").
    :return: Lista de dispositivos detectados.
    """
    logging.debug(f"Escaneando el rango: {network_range}")
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=network_range, arguments='-sn')  # Escaneo tipo ping
        devices = []
        connections = []
        for host in nm.all_hosts():
            device_info = {
                "ip": host,
                "hostname": nm[host].hostname(),
                "state": nm[host].state()
            }
        
        # Detectar conexiones: asumimos que si los enrutadores están en el mismo rango, están conectados
        for other_host in nm.all_hosts():
            if host != other_host:
                # Verifica si los enrutadores están en la misma subred (esto puede depender de la lógica de red)
                # Ejemplo simplificado: si están en el mismo rango de IP, asumimos que están conectados
                connections.append({
                    "from": host,
                    "to": other_host
                })
        
        logging.debug(f"Dispositivos detectados: {devices}")
        logging.debug(f"Conexiones detectadas: {connections}")
        return {
            "devices": devices,
            "connections": connections
        }
    except Exception as e:
        logging.error(f"Error al escanear la red: {str(e)}")
        return {"error": str(e)}


def update_topology(network_range):
    """
    Actualiza la topología global con los dispositivos encontrados y la guarda en un archivo.
    """
    global current_topology
    logging.debug("Actualizando la topología...")
    current_topology = scan_network(network_range)
    # Guardar la topología en un archivo JSON
    with open("current_topology.json", "w") as f:
        json.dump(current_topology, f)
    logging.debug(f"Topología actualizada y guardada en archivo: {current_topology}")


def start_topology_daemon(network_range):
    """
    Inicia un demonio que explora la red periódicamente.
    :param network_range: Rango de red.
    """
    global daemon_running, daemon_thread, daemon_interval, stop_event

    if daemon_running:
        logging.debug("El demonio ya está corriendo.")
        return {"error": "Daemon is already running"}

    daemon_running = True
    stop_event.clear()  # Asegúrate de que el evento esté limpio

    def daemon_task():
        while daemon_running:
            logging.debug("El demonio está actualizando la topología...")
            update_topology(network_range)
            # Espera el intervalo o detiene el hilo si el evento es activado
            if stop_event.wait(daemon_interval):
                break

    logging.debug("Iniciando el demonio...")
    daemon_thread = threading.Thread(target=daemon_task, daemon=True)
    daemon_thread.start()
    logging.debug("Demonio iniciado.")
    return {"message": "Daemon started", "interval": daemon_interval}


def stop_topology_daemon():
    """
    Detiene el demonio que explora la red.
    """
    global daemon_running, daemon_thread, stop_event

    if not daemon_running:
        logging.debug("El demonio no está corriendo.")
        return {"error": "Daemon is not running"}

    logging.debug("Deteniendo el demonio...")
    daemon_running = False
    stop_event.set()  # Activa el evento para interrumpir el `wait`

    if daemon_thread and daemon_thread.is_alive():
        logging.debug("Esperando a que el hilo termine...")
        daemon_thread.join()
        logging.debug("Hilo terminado.")
        daemon_thread = None

    logging.debug("Demonio detenido.")
    return {"message": "Daemon stopped"}


def set_daemon_interval(interval):
    """
    Cambia el intervalo de tiempo del demonio.
    :param interval: Nuevo intervalo en segundos.
    """
    global daemon_interval
    logging.debug(f"Cambiando el intervalo del demonio a {interval} segundos.")
    daemon_interval = interval
    return {"message": f"Interval set to {interval} seconds"}

def generate_topology_graph(network_range):
    """
    Genera un gráfico de la topología utilizando networkx.
    """
    try:
        # Llamamos a scan_network para obtener los dispositivos y sus conexiones
        topology_data = scan_network(network_range)

        # Si no hay dispositivos o hay un error
        if "error" in topology_data:
            logging.error(f"Error en el escaneo de red: {topology_data['error']}")
            return None
        
        devices = topology_data["devices"]
        connections = topology_data["connections"]

        # Crear el grafo
        G = nx.Graph()

        # Agregar nodos a la red (enrutadores)
        for device in devices:
            G.add_node(device["ip"], label=device.get("hostname", device["ip"]))

        # Agregar conexiones entre los dispositivos
        for connection in connections:
            G.add_edge(connection["from"], connection["to"])

        # Dibujar la red
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue")

        # Dibujar las etiquetas con los nombres de los nodos
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels)

        # Guardar el gráfico en un directorio conocido
        output_dir = os.path.join(os.getcwd(), "static")
        os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe
        graph_path = os.path.join(output_dir, "topology_graph.png")
        plt.savefig(graph_path)
        plt.close()

        logging.info(f"Gráfico de la topología guardado en: {graph_path}")
        return graph_path
    
    except Exception as e:
        logging.error(f"Error al generar el gráfico de topología: {str(e)}")
        return None