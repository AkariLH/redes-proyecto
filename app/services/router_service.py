from app.models.router import Router, Interface

# Datos de ejemplo para usuarios
users_router1 = [
    {"username": "admin", "permissions": "read-write"},
    {"username": "guest", "permissions": "read-only"},
]

users_router2 = [
    {"username": "operator", "permissions": "read-write"},
]

# Enrutadores con datos de ejemplo
routers = [
    Router("router1", "10.0.0.1", "192.168.1.1", "Core", "Cisco", "IOS", ["eth0", "eth1"], None, users_router1),
    Router("router2", "10.0.0.2", "192.168.1.2", "Edge", "Juniper", "JunOS", ["eth0"], None, users_router2),
]

# --- Funciones de Gestión de Enrutadores ---
def get_all_routers():
    """Devuelve la información de todos los enrutadores."""
    return [router.to_dict() for router in routers]

def get_router_by_hostname(hostname):
    """Devuelve la información de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            return router.to_dict()
    return None

def get_interfaces_by_router(hostname):
    """Devuelve las interfaces de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            return [interface.to_dict() for interface in router.interfaces]
    return None

# --- Funciones de Gestión de Usuarios por Enrutador ---
def get_users_by_router(hostname):
    """Devuelve los usuarios de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            return router.users
    return None

def add_user_to_router(hostname, username, permissions):
    """Agrega un nuevo usuario a un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            user = {"username": username, "permissions": permissions}
            router.users.append(user)
            return user
    return None

def update_user_in_router(hostname, username, permissions):
    """Actualiza un usuario en un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            for user in router.users:
                if user["username"] == username:
                    user["permissions"] = permissions
                    return user
    return None

def delete_user_from_router(hostname, username):
    """Elimina un usuario de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            router.users = [user for user in router.users if user["username"] != username]
            return {"message": f"User '{username}' deleted from router '{hostname}'"}
    return None
