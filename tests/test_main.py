from main import get_parameters, update_main, update_sec
from unittest.mock import MagicMock

def test_get_parameters():
    cpu, ram_av, ram_tot, disk_av, disk_tot = get_parameters()
    assert isinstance(cpu, float)
    assert isinstance(ram_av, float)
    assert isinstance(ram_tot, float)
    assert isinstance(disk_av, float)
    assert isinstance(disk_tot, float)
    assert 0 <= cpu <= 100
    assert ram_av >= 0
    assert ram_tot >= 0
    assert disk_av >= 0
    assert disk_tot >= 0

def test_update_main():
    window = MagicMock()
    update_main(window)
    # Проверяем, что методы update были вызваны
    window.__getitem__.assert_called()  # Проверяем, что элементы окна были обновлены

def test_update_sec():
    window = MagicMock()
    update_sec(window)
    # Проверяем, что методы update были вызваны
    window.__getitem__.assert_called()  # Проверяем, что элементы окна были обновлены