import pytest
from services.port_service import PortService

def test_get_ports_info_runs():
    ports = PortService.get_ports_info()
    assert isinstance(ports, list)
    for entry in ports:
        assert 'name' in entry
        assert 'port' in entry

def test_get_ports_info_runs_service():
    ports = PortService.get_ports_info()
    assert isinstance(ports, list)
    for entry in ports:
        assert 'name' in entry
        assert 'port' in entry
