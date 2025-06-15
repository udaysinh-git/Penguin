import psutil
import socket


class PortService:
    """
    Service to retrieve running services and their listening ports.
    Cross-platform: works on Linux and Windows.
    """

    @staticmethod
    def get_ports_info():
        """
        Returns a list of dicts: [{'name': process_name, 'port': port_number}]
        """
        ports = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status != psutil.CONN_LISTEN:
                continue
            laddr = conn.laddr
            if len(laddr) < 2:
                continue
            port = laddr[1]
            pid = conn.pid
            if pid is None:
                continue
            try:
                proc = psutil.Process(pid)
                name = proc.name()
            except Exception:
                name = "Unknown"
            ports.append({'name': name, 'port': port})
        # Remove duplicates (same process/port)
        seen = set()
        unique_ports = []
        for entry in ports:
            key = (entry['name'], entry['port'])
            if key not in seen:
                unique_ports.append(entry)
                seen.add(key)
        return unique_ports

    @staticmethod
    def get_local_ip():
        """
        Returns the local IP address of the current machine.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
