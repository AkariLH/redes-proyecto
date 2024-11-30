class User:
    def __init__(self, username, permissions, devices=None):
        self.username = username
        self.permissions = permissions
        self.devices = devices or []

    def to_dict(self):
        """Convierte el objeto User a un diccionario para facilitar su serialización."""
        return {
            "username": self.username,
            "permissions": self.permissions,
            "devices": self.devices,
        }
 
