from app.models.user import User

# Lista para almacenar los usuarios (almacenamiento temporal)
users = []

def get_users():
    """Obtiene la lista de todos los usuarios."""
    return [user.to_dict() for user in users]

def add_user(username, permissions, devices=None):
    """Agrega un nuevo usuario."""
    user = User(username, permissions, devices)
    users.append(user)
    return user.to_dict()

def update_user(username, permissions=None, devices=None):
    """Actualiza un usuario existente."""
    for user in users:
        if user.username == username:
            if permissions:
                user.permissions = permissions
            if devices is not None:
                user.devices = devices
            return user.to_dict()
    return None

def delete_user(username):
    """Elimina un usuario existente."""
    global users
    users = [user for user in users if user.username != username]
    return {"message": f"User '{username}' deleted"}
 
