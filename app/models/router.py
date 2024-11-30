class Router:
    def __init__(self, hostname, loopback_ip, admin_ip, role, company, os, active_interfaces=None, interfaces=None, users=None):
        self.hostname = hostname
        self.loopback_ip = loopback_ip
        self.admin_ip = admin_ip
        self.role = role
        self.company = company
        self.os = os
        self.active_interfaces = active_interfaces or []
        self.interfaces = interfaces or []
        self.users = users or []  # Lista de usuarios asociados al enrutador

    def to_dict(self):
        """Convierte el objeto Router a un diccionario."""
        return {
            "hostname": self.hostname,
            "loopback_ip": self.loopback_ip,
            "admin_ip": self.admin_ip,
            "role": self.role,
            "company": self.company,
            "os": self.os,
            "active_interfaces": self.active_interfaces,
            "interfaces": [interface.to_dict() for interface in self.interfaces],
            "users": self.users,  # Devuelve los usuarios como están
        }

class Interface:
    def __init__(self, type_, number, ip, subnet_mask, status, connected_router=None):
        self.type_ = type_
        self.number = number
        self.ip = ip
        self.subnet_mask = subnet_mask
        self.status = status
        self.connected_router = connected_router

    def to_dict(self):
        """Convierte el objeto Interface a un diccionario."""
        return {
            "type": self.type_,
            "number": self.number,
            "ip": self.ip,
            "subnet_mask": self.subnet_mask,
            "status": self.status,
            "connected_router": self.connected_router,
        }
