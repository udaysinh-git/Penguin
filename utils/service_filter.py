from config.settings import SERVICE_FILTER_PATH

def get_service_filter():
    """
    Reads the service_filter.txt file and returns a set of service names to filter.
    Ignores empty lines and lines starting with '#'.
    """
    try:
        with open(SERVICE_FILTER_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        services = {
            line.strip() for line in lines
            if line.strip() and not line.strip().startswith("#")
        }
        return services
    except FileNotFoundError:
        return set()
