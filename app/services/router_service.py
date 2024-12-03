from app.models.router import Router, Interface

# Lista de enrutadores detectados
routers = []

# Diccionario para almacenar usuarios por enrutador
users_per_router = {}

# --- Excepciones ---
class RouterNotFoundError(Exception):
    """Excepción personalizada para manejar cuando un enrutador no es encontrado."""
    def __init__(self, hostname):
        self.message = f"ERROR 404: Router '{hostname}' not found"
        super().__init__(self.message)

class InterfaceNotFoundError(Exception):
    """Excepción personalizada para manejar cuando una interfaz no es encontrada."""
    def __init__(self, interface_name):
        self.message = f"ERROR 404: Interface '{interface_name}' not found"
        super().__init__(self.message)

class UserNotFoundError(Exception):
    """Excepción personalizada para manejar cuando un usuario no es encontrado en un enrutador."""
    def __init__(self, username, hostname):
        self.message = f"ERROR 404: User '{username}' not found in router '{hostname}'"
        super().__init__(self.message)

# --- Funciones de Gestión de Enrutadores ---
def get_all_routers():
    """Devuelve la información de todos los enrutadores."""
    return [router.to_dict() for router in routers]

def get_router_by_hostname(hostname):
    """Devuelve la información de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            return router.to_dict()
    raise RouterNotFoundError(hostname)

def get_interfaces_by_router(hostname):
    """Devuelve las interfaces de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            return [interface.to_dict() for interface in router.interfaces]
    raise RouterNotFoundError(hostname)

# --- Funciones de Gestión de Usuarios por Enrutador ---
def get_users_by_router(hostname):
    """Devuelve los usuarios de un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            return router.users
    raise RouterNotFoundError(hostname)

def add_user_to_router(hostname, username, permissions):
    """Agrega un nuevo usuario a un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            user = {"username": username, "permissions": permissions}
            router.users.append(user)
            return user
    raise RouterNotFoundError(hostname)

def update_user_in_router(hostname, username, permissions):
    """Actualiza un usuario en un enrutador específico."""
    for router in routers:
        if router.hostname == hostname:
            for user in router.users:
                if user["username"] == username:
                    user["permissions"] = permissions
                    return user
            raise UserNotFoundError(hostname)
    raise RouterNotFoundError(hostname)

def delete_user_from_router(hostname, username):
    """Elimina un usuario de un enrutador específico."""
    #for router in routers:
    #    if router.hostname == hostname:
    #        router.users = [user for user in router.users if user["username"] != username]
    #        return {"message": f"User '{username}' deleted from router '{hostname}'"}
    
    for router in routers:
        if router.hostname == hostname:
            for user in router.users:
                if user["username"] == username:
                    router.users = [u for u in router.users if u["username"] != username]
                    return {"message": f"User '{username}' deleted from router '{hostname}'"}
            raise UserNotFoundError(username, hostname)
    raise RouterNotFoundError(hostname)