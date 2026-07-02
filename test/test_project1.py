import pytest
from project_1_vending_engine.vending_engine import VendingMetricEngine

#============Test Class Boundry===================================
@pytest.fixture
def engine():
    e = VendingMetricEngine()
    e.add_incoming_data("machine_alpha", "soda", 2.50, 2)
    e.add_incoming_data("machine_beta", "chips", 1.50, 1)
    return e

def test_machine_isolation(engine):
    snapshot = engine.inventory_snapshot
    assert "soda" not in snapshot["machine_beta"]["items_sold"]
    assert snapshot["machine_beta"]["total_revenue"] == 1.50

def test_encapsulation_shield(engine):
    snapshot = engine.inventory_snapshot
    snapshot.clear()
    assert "machine_alpha" in engine.inventory_snapshot

#======================Happy Path=====================================
def test_revenue_calculation():
    engine = VendingMetricEngine()
    engine.add_incoming_data("machine_alpha", "soda", 2.50, 2)
    assert engine.inventory_snapshot["machine_alpha"]["total_revenue"] == 5.0
    assert not engine.inventory_snapshot["machine_alpha"]["items_sold"] == "chips"

def test_invalid_quantity_raises():
    engine = VendingMetricEngine()
    with pytest.raises(ValueError):
        engine.add_incoming_data("machine_alpha", "soda", 2.50, -1)

def test_same_item_added_twice_accumulates():
    engine = VendingMetricEngine()
    engine.add_incoming_data("machine_alpha", "soda", 2.50, 2)
    engine.add_incoming_data("machine_alpha", "soda", 2.50, 1)
    assert engine.inventory_snapshot["machine_alpha"]["items_sold"]["soda"] == 3
    assert engine.inventory_snapshot["machine_alpha"]["total_revenue"] == 7.50


@pytest.mark.parametrize("machine_id, item_name, price, quantity, expected", [
    ("machine_alpha", "chips", 2.50, 2, 5.0),
    ("machine_beta",  "soda",  1.75, 4, 7.0),
    ("machine_gamma", "water", 0.50, 10, 5.0),
])
def test_revenue_happy_path(machine_id, item_name, price, quantity, expected):
    engine = VendingMetricEngine()
    engine.add_incoming_data(machine_id, item_name, price, quantity)
    snapshot = engine.inventory_snapshot
    assert snapshot[machine_id]["total_revenue"] == expected

@pytest.mark.parametrize("machine_id, item_name, price, quantity", [
    (1,            "chips", 2.50,  2),   # machine_id not string
    ("machine_alpha", 123,  2.50,  2),   # item_name not string
    ("machine_alpha", "chips", -1, 2),   # negative price
    ("machine_alpha", "chips", 2.50, 0), # zero quantity
])
def test_invalid_inputs_raise(machine_id, item_name, price, quantity):
    engine = VendingMetricEngine()
    with pytest.raises(ValueError):
        engine.add_incoming_data(machine_id, item_name, price, quantity)